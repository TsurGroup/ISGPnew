from pathlib import Path
from data_base.algorithm_parameters import create_algorithm_parameters_table
from data_base.experiment_data import create_experiment_table
from data_base.genomes import create_genomes_table
from cache.cache import delete_cache
from file_managment.file_manager import PROJECTS_DIR, check_if_path_exists, get_project_path
from cache.db_connection import create_db, get_db_path#, initialize_db_connection




def create_new_project(project_name):

    delete_cache()
    #project_path = get_project_path(project_name)
    db_path = get_db_path()
    print(db_path)
    if check_if_path_exists(db_path):
        return False
    
    status = create_db()
    create_experiment_table()
    create_genomes_table()
    create_algorithm_parameters_table()

    return status

def get_project_names():
    if not check_if_path_exists(PROJECTS_DIR):
        return []
    
    # List all directories inside the "projects" folder
    projects = [p.name for p in Path(PROJECTS_DIR).iterdir() if p.is_dir()]
    
    return projects

def load_project(project_name):
    project_path = get_project_path()
    return check_if_path_exists(project_path)
