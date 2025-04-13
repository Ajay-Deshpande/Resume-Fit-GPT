from setuptools import setup, find_packages

setup(
    name="ResumeGPT",
    version="2.0",
    description="An LLM fits the resume for the job description. Sit back, relax and apply.",
    author="Ajay Deshpande",
    author_email="deshpande.ajay.us@gmail.com",
    url="https://github.com/Ajay-Deshpande/ResumeGPT",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.9.3",
        "configparser>=5.0.2",
        "langchain==0.1.20",
        "langchain-ollama==0.3.0",
        "langchain-core==0.1.52",
        "pydantic==2.7.1",
        "reportlab>=3.5.59",
        "requests>=2.25.1",
        "ruamel.yaml>=0.16.12",
        "pytest>=8.2.2",
        "free-proxy>=1.1.1",
        "Jinja2==3.1.4",
        "PyYAML==5.3.1",
        "pytest-cov==5.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
