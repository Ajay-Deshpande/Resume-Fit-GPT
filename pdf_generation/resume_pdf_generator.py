import configparser
import json
import os
import random
from .. import config
from .. import utils
import subprocess
import yaml

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Table,
    TableStyle,
    Spacer,
    HRFlowable,
)
from . import resume_pdf_styles


class ResumePDFGenerator:
    """
    A class to generate a resume PDF from JSON data using the ReportLab library.
    """

    def __init__(self):
        """
        Initialize the ResumePDFGenerator by registering fonts.
        """
        self._register_fonts()

    def _register_fonts(self):
        """
        Register fonts for use in the PDF.
        """
        for style, path in resume_pdf_styles.FONT_PATHS.items():
            pdfmetrics.registerFont(
                ttfonts.TTFont(resume_pdf_styles.FONT_NAMES[style], path)
            )

    def _append_section_table_style(self, table_styles, row_index):
        """
        Append styles for section headers in the table.

        Args:
            table_styles (list): List of table styles to be extended.
            row_index (int): The current row index in the table.
        """
        table_styles.extend(
            [
                ("TOPPADDING", (0, row_index), (1, row_index), 5),
                ("BOTTOMPADDING", (0, row_index), (1, row_index), 2),
                ("LINEBELOW", (0, row_index), (-1, row_index), 0.1, colors.black),
            ]
        )

    def _add_table_row(
        self,
        table_data,
        table_styles,
        row_index,
        content_style_map,
        span=False,
        padding=resume_pdf_styles.DEFAULT_PADDING,
        bullet_point=None,
    ):
        """
        Add a row to the table data and update the table styles.

        Args:
            table_data (list): The table data to be extended.
            table_styles (list): The table styles to be extended.
            row_index (int): The current row index in the table.
            content_style_map (list of tuples): A list of tuples where each tuple contains content and its corresponding style.
            span (bool, optional): Whether the row should span across columns. Defaults to False.
            padding (tuple, optional): The top and bottom padding for the row. Defaults to (1, 1).
            bullet_point (str, optional): The bullet point to prepend to the content.
            spacer_height (int, optional): The height of the spacer to add after the row. Defaults to None.
        """
        if bullet_point:
            table_data.append(
                [
                    Paragraph(content, bulletText=bullet_point, style=style)
                    for content, style in content_style_map
                ]
            )
        else:
            table_data.append(
                [Paragraph(content, style) for content, style in content_style_map]
            )
        table_styles.extend(
            [
                ("BOTTOMPADDING", (0, row_index), (-1, row_index), padding[0]),
                ("TOPPADDING", (0, row_index), (-1, row_index), padding[1]),
            ]
        )
        if span:
            table_styles.append(("SPAN", (0, row_index), (1, row_index)))

        row_index += 1

        return row_index

    def add_experiences(self, table_data, table_styles, row_index, experiences):
        """
        Add experiences section to the resume.

        Args:
            table_data (list): The table data to be extended.
            table_styles (list): The table styles to be extended.
            row_index (int): The current row index in the table.
            experiences (list): The list of experiences to be added.
        """
        row_index = self._add_table_row(
            table_data=table_data,
            table_styles=table_styles,
            row_index=row_index,
            content_style_map=[
                ("Experience", resume_pdf_styles.PARAGRAPH_STYLES["section"])
            ],
            span=True,
        )
        self._append_section_table_style(table_styles, row_index - 1)

        for idx, job in enumerate(experiences):
            # Create a duration string from startdate and enddate
            duration = f"{job['titles'][0]['startdate']}-{job['titles'][0]['enddate']}"

            row_index = self._add_table_row(
                table_data=table_data,
                table_styles=table_styles,
                row_index=row_index,
                content_style_map=[
                    (
                        job["company"],
                        resume_pdf_styles.PARAGRAPH_STYLES["company_heading"],
                    ),
                    (duration, resume_pdf_styles.PARAGRAPH_STYLES["company_duration"]),
                ],
            )

            row_index = self._add_table_row(
                table_data=table_data,
                table_styles=table_styles,
                row_index=row_index,
                content_style_map=[
                    (
                        job["titles"][0]["name"],
                        resume_pdf_styles.PARAGRAPH_STYLES["company_title"],
                    ),
                    (
                        job["location"],
                        resume_pdf_styles.PARAGRAPH_STYLES["company_location"],
                    ),
                ],
            )

            for i, bullet_point in enumerate(job["highlights"]):
                style = (
                    resume_pdf_styles.PARAGRAPH_STYLES["last_bullet_point"]
                    if i == len(job["highlights"]) - 1
                    else resume_pdf_styles.PARAGRAPH_STYLES["bullet_points"]
                )
                padding = (0, 1)
                if i == len(job["highlights"]) - 1:
                    padding = (5, 1)
                row_index = self._add_table_row(
                    table_data=table_data,
                    table_styles=table_styles,
                    bullet_point="•",
                    row_index=row_index,
                    content_style_map=[
                        (
                            bullet_point,
                            style,
                        )
                    ],
                    span=True,
                    padding=padding,
                )

        return row_index

    def add_education(self, table_data, table_styles, row_index, education):
        """
        Add education section to the resume.

        Args:
            table_data (list): The table data to be extended.
            table_styles (list): The table styles to be extended.
            row_index (int): The current row index in the table.
            education (list): The list of education entries to be added.
        """
        row_index = self._add_table_row(
            table_data=table_data,
            table_styles=table_styles,
            row_index=row_index,
            content_style_map=[
                ("Education", resume_pdf_styles.PARAGRAPH_STYLES["section"])
            ],
            span=True,
        )
        self._append_section_table_style(table_styles, row_index - 1)

        for edu in education:
            degrees = ", ".join(edu["degrees"][0]["names"])
            row_index = self._add_table_row(
                table_data=table_data,
                table_styles=table_styles,
                row_index=row_index,
                content_style_map=[
                    (
                        f"<font name='{resume_pdf_styles.FONT_NAMES['bold']}'>{edu['school']}</font>, {degrees}",
                        resume_pdf_styles.PARAGRAPH_STYLES["education"],
                    )
                ],
                span=True,
            )
        return row_index

    def add_skills(self, table_data, table_styles, row_index, skills):
        """
        Add skills section to the resume.

        Args:
            table_data (list): The table data to be extended.
            table_styles (list): The table styles to be extended.
            row_index (int): The current row index in the table.
            skills (list): The list of skills to be added.
        """
        row_index = self._add_table_row(
            table_data=table_data,
            table_styles=table_styles,
            row_index=row_index,
            content_style_map=[
                ("Skills", resume_pdf_styles.PARAGRAPH_STYLES["section"])
            ],
            span=True,
        )
        self._append_section_table_style(table_styles, row_index - 1)

        for group in skills:
            group_keys = list(group.keys())
            skill_type = group[group_keys[0]]
            skills_list = group[group_keys[1]]
            skills_str = ", ".join(skills_list)
            formatted_skills = f"<font name='{resume_pdf_styles.FONT_NAMES['bold']}'>{skill_type}</font>: {skills_str}"
            row_index = self._add_table_row(
                table_data=table_data,
                table_styles=table_styles,
                row_index=row_index,
                content_style_map=[
                    (formatted_skills, resume_pdf_styles.PARAGRAPH_STYLES["skills"])
                ],
                span=True,
                padding=(2, 2),
            )
        return row_index

    def generate_resume(self, job_data_location, data):
        """
        Generate a resume PDF from JSON data.

        Args:
            job_data_location (str): The path where the PDF will be saved.
            data (dict): The JSON data containing resume information.
        """
        email = data["basic"]["contact"]["email"]
        name = data["basic"]["name"]
        phone = data["basic"]["contact"]["phone"]

        def clean_url(url):
            return (
                url.replace("https://", "").replace("http://", "").replace("www.", "")
            )

        linkedin = next(
            (
                clean_url(site["url"])
                for site in data["basic"]["websites"]
                if site["icon"] == "linkedin"
            ),
            "",
        )
        github = next(
            (
                clean_url(site["url"])
                for site in data["basic"]["websites"]
                if site["icon"] == "github"
            ),
            "",
        )
        address = ", ".join(data["basic"]["address"])
        doc, pdf_location = resume_pdf_styles.generate_doc_template(
            name, job_data_location
        )
        table_data = []
        table_styles = []
        row_index = 0

        if data.get("debug", False):
            table_styles.append(resume_pdf_styles.DEBUG_STYLE)

        table_styles.extend(resume_pdf_styles.DOCUMENT_ALIGNMENT)

        # Add name and contact information
        row_index = self._add_table_row(
            table_data=table_data,
            table_styles=table_styles,
            row_index=row_index,
            content_style_map=[(name, resume_pdf_styles.PARAGRAPH_STYLES["name"])],
            span=True,
        )

        row_index = self._add_table_row(
            table_data=table_data,
            table_styles=table_styles,
            row_index=row_index,
            content_style_map=[
                (
                    f"{email} | {phone} | {linkedin} | {github} | {address}",
                    resume_pdf_styles.PARAGRAPH_STYLES["contact"],
                )
            ],
            span=True,
        )

        # Add objective
        row_index = self._add_table_row(
            table_data=table_data,
            table_styles=table_styles,
            row_index=row_index,
            content_style_map=[
                ("Objective", resume_pdf_styles.PARAGRAPH_STYLES["section"])
            ],
            span=True,
        )
        self._append_section_table_style(table_styles, row_index - 1)

        row_index = self._add_table_row(
            table_data=table_data,
            table_styles=table_styles,
            row_index=row_index,
            content_style_map=[
                (data["objective"], resume_pdf_styles.PARAGRAPH_STYLES["objective"])
            ],
            span=True,
        )

        # Add experience
        row_index = self.add_experiences(
            table_data=table_data,
            table_styles=table_styles,
            row_index=row_index,
            experiences=data["experiences"],
        )

        # Add education
        row_index = self.add_education(
            table_data=table_data,
            table_styles=table_styles,
            row_index=row_index,
            education=data["education"],
        )

        # Add skills
        row_index = self.add_skills(
            table_data=table_data,
            table_styles=table_styles,
            row_index=row_index,
            skills=data["skills"],
        )

        table = Table(
            table_data,
            colWidths=[
                resume_pdf_styles.FULL_COLUMN_WIDTH * 0.75,
                resume_pdf_styles.FULL_COLUMN_WIDTH * 0.3,
            ],
            spaceBefore=0,
            spaceAfter=0,
        )
        table.setStyle(TableStyle(table_styles))

        doc.build([table])
        return pdf_location

    def generate_pdf_from_resume_yaml(self, yaml_path, job_data_location):
        """
        Generate a resume PDF from YAML data.

        Args:
            yaml_path (str): The path to the YAML file containing resume information.
            job_data_location (str): The path where the PDF will be saved.
        """
        return self.generate_resume(
            job_data_location, utils.read_yaml(filename=yaml_path)
        )
