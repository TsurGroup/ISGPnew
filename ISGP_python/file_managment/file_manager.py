import sys
from pathlib import Path
from project_context import current_project_name


def get_base_dir():
    """Determine the base directory of the project."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent.resolve()
    else:
        return Path(__file__).parent.parent.resolve()

# Base directory
BASE_DIR = get_base_dir()

# Projects directory (ensure it's created at startup)
PROJECTS_DIR = BASE_DIR / "projects"
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)  # Create once at initialization

def check_if_path_exists(path):
    """Check if a given path exists."""
    return Path(path).exists()


def get_projects_dir():
    """Return the path to the projects directory."""
    return PROJECTS_DIR


def get_config_path():
    """Get the path to the config.json file."""
    config_path = BASE_DIR / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    return config_path


def get_project_path():
    """Get the path for a specific project."""
    project_name = current_project_name.get()
    if not project_name:
        raise ValueError("Project name is not set in current_project_name.")
    project_path = PROJECTS_DIR / project_name
    project_path.mkdir(parents=True, exist_ok=True)  # Create only if needed
    return project_path


def get_db_path():
    """Get the path for the SQLite database of a specific project."""
    project_name = current_project_name.get()
    if not project_name:
        raise ValueError("Project name is not set in current_project_name.")
    return get_project_path() / f"{project_name}.db"


def get_excel_path():
    """Get the path for the Excel file of a specific project."""
    project_name = current_project_name.get()
    if not project_name:
        raise ValueError("Project name is not set in current_project_name.")
    return get_project_path() / f"{project_name}.xlsx"

def get_example_excel_file_path():
    return ''
def get_example_text_file_path():
    return ''
