import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cache.db_connection import create_db
from tests.genetic_algorithm_test import generate_evolution_test
from modules.home_module.home_handler import create_new_project
from file_managment.file_manager import get_base_dir
from tests.test_data import test_project_name
from data_base.algorithm_parameters import create_algorithm_parameters_table
from data_base.experiment_data import create_experiment_table
from data_base.genomes import create_genomes_table


BASE_DIR = get_base_dir()
PROJECTS_DIR = BASE_DIR / "projects"
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)  # Create once at initialization
create_new_project(test_project_name)
status = create_db()
create_experiment_table()
create_genomes_table()
create_algorithm_parameters_table()


if __name__ == "__main__":
    generate_evolution_test()
