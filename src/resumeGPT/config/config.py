import logging
import os
from pathlib import Path
from langchain_ollama.llms import OllamaLLM
import importlib.resources

PACKAGE_NAME = 'resumeGPT'
RESOURCES_DIR_NAME = 'Resources'

# Define the names of the YAML files inside 'resources'
PROMPTS_YAML_FILENAME = 'prompts.yaml' # <-- Make sure these match your filenames
DESCRIPTIONS_YAML_FILENAME = 'descriptions.yaml' # <-- Make sure these match your filenames


RESOURCES_PATH: Path | None = None
PROMPTS_YAML: str | None = None
DESCRIPTIONS_YAML: str | None = None
package_root_path = importlib.resources.files(PACKAGE_NAME)
# Join the package root path with the name of the resources directory
RESOURCES_PATH = (package_root_path / RESOURCES_DIR_NAME).resolve()
PROMPTS_YAML = (package_root_path / "prompts/prompts.yaml").resolve()
DESCRIPTIONS_YAML = (package_root_path / "prompts/extractor_descriptions.yaml").resolve()

# Initialize logger
logger = logging.getLogger(__name__)

# Define project paths
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKGROUND_TASKS_LOG = os.path.join(PROJECT_PATH, "background_tasks", "tasks.log")
if not os.path.exists(os.path.join(PROJECT_PATH, "background_tasks")):
    os.makedirs(os.path.join(PROJECT_PATH, "background_tasks"))

REQUESTS_HEADERS = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

# Define model configuration
CHAT_MODEL = OllamaLLM
MODEL_NAME = "llama3.1"
TEMPERATURE = 0.3
OPEN_FILE_COMMAND = "code -r"
MAX_CONCURRENT_WORKERS = 4
MAX_RETRIES = 3
BACKOFF_FACTOR = 5