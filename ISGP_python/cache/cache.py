from config.env import get_env
from data_base.algorithm_parameters import get_algorithm_parameters_from_db
from data_base.experiment_data import get_experiment_data_db
from data_base.genomes import get_discrepencies_from_db
from modules.experiment_data_module.constant_data import calculate_constant_data
from tests.test_data import dummy_experiment_data, dummy_algorithm_parameters


from models.experiment_data import ExperimentData
from models.project import AlgorithmParameters
from models.project_data import ProjectConstants, ProjectStatus

EXPERIMENT_DATA= 'EXPERIMENT_DATA'
PROJECT_STATUS = 'PROJECT_STATUS'
PROJECTS_CONSTANTS = 'PROJECTS_CONSTANTS'
DISCREPANCIES='DISCREPANCIES'
ALGORITHM_PARAMETERS='ALGORITHM_PARAMETERS'

cache = {}

def delete_cache():
     return cache.clear()

def get_project_status()-> ProjectStatus:
     return cache.get(PROJECT_STATUS)

def set_project_status(status:ProjectStatus):
    cache[PROJECT_STATUS] = status



def get_project_constants_from_cache() -> ProjectConstants:
      
      if PROJECTS_CONSTANTS not in cache:  
         expermint_data1  = get_experiment_data(0)
         expermint_data2  = get_experiment_data(1)
         algorithm_parameters = get_algorithm_parameters_from_cache()
         project_constants = calculate_constant_data(expermint_data1,expermint_data2,algorithm_parameters) 
         set_project_constants(project_constants)

      return cache.get(PROJECTS_CONSTANTS)


def set_project_constants(project_constants:ProjectConstants):       
       cache[PROJECTS_CONSTANTS] = project_constants


def delete_project_constants_cache() -> None:
    """Deletes a specific key from the cache."""
    if PROJECTS_CONSTANTS in cache:
        del cache[PROJECTS_CONSTANTS]


def get_experiment_data(id) -> ExperimentData:
    if get_env() == "test":
        return dummy_experiment_data

    key = EXPERIMENT_DATA + str(id)

    if key not in cache:
        set_experiment_data(id)

    return cache.get(key)

def set_experiment_data(id):

    experiment_data = get_experiment_data_db(id)
    key = EXPERIMENT_DATA+str(id)
    cache[key] = experiment_data


def get_algorithm_parameters_from_cache() -> AlgorithmParameters:
    if get_env() == "test":
        # Return dummy AlgorithmParameters for testing
        return dummy_algorithm_parameters

    if ALGORITHM_PARAMETERS not in cache:
        algorithm_parameters = get_algorithm_parameters_from_db()
        set_algorithm_parameters_cache(algorithm_parameters)

    return cache[ALGORITHM_PARAMETERS]

def set_algorithm_parameters_cache(algorithm_parameters:AlgorithmParameters):
    if algorithm_parameters is None:
        return None
    cache[ALGORITHM_PARAMETERS] = algorithm_parameters



def get_discrepancies(run:int,generation:int):

    discrepencies = get_discrepencies_from_db(run,generation)
    return discrepencies



def add_discrepancies(new_discrepancies,run:int,generation:int):
    key = DISCREPANCIES+str(run)+str(generation)
    if key in cache.keys():
       cache[key] = cache[key] + new_discrepancies
    else:
        cache[key] =  new_discrepancies




def delete_discrepancies():
     if DISCREPANCIES in cache.keys():
       del cache[DISCREPANCIES]
     else:
         return