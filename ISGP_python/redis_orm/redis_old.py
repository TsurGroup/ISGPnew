import datetime
import json
import numpy as np
import redis
import uuid
from models.experiment_data import ExperimentData, ExperimentDataView
from models.functions.function import FunctionParameters
from models.project_data import ProjectConstants, ProjectStatus
from modules.genetic_algorithm.genome_parameters import Genome

from redis_orm.redis_keys import BEST_MODELS, DATA_SET, DISCREPANCY, FITNESS, FUNCTION_PARAMATERS, LOGARITHMIC_RELAXATION_TIME, POPULATION, PROJECT_STATUS, PROJECTS_CONSTANTS, TIME_CREATED

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)



def new_project():
   session_id = str(uuid.uuid4())

   current_datetime = datetime.datetime.now()
   current_datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

   redis_client.hmset(session_id,{TIME_CREATED:current_datetime_string})
   return session_id

def get_name(session_id):
   if (redis_client.exists(session_id)):
      name = redis_client.hget(session_id, 'name')
      #print(name)
      return name
   else:
      return ''
  
def save_experiment_data_to_redis(session_id,experiment_data_list:list[ExperimentData]):

  data_to_save = {f'{DATA_SET+str(idx)}':  json.dumps(data.to_dict()) for idx, data in enumerate(experiment_data_list)}
    
  redis_client.hmset(session_id, data_to_save)
  #experiment_data = ExperimentDataView(experiment_data_list[0],experiment_data_list[1])

  return 1 #experiment_data


def save_project(session_id,experiment_data_list:list[ExperimentData]):

  data_to_save = {f'{DATA_SET+str(idx)}':  json.dumps(data.to_dict()) for idx, data in enumerate(experiment_data_list)}
    
  redis_client.hmset(session_id, data_to_save)
  experiment_data = ExperimentDataView(experiment_data_list[0],experiment_data_list[1])

  return experiment_data

def set_function_parameters(user_id, parameters :FunctionParameters):
    parameters_json = json.dumps(parameters.dict())
    #print(parameters_json)
    redis_client.hmset(user_id, {FUNCTION_PARAMATERS: parameters_json})
    return 1

def get_function_parameters(user_id):
    data_from_redis = redis_client.hget(user_id,FUNCTION_PARAMATERS)
    data_dict = json.loads(data_from_redis)
    #print(data_dict)
    return FunctionParameters(**data_dict)
    

def set_population(user_id, population: list[Genome]):
    population_json = json.dumps([genome.to_dict(include_subclasses=True) for genome in population])
    #print(population_json)
    redis_client.hmset(user_id, {POPULATION: population_json})
    return 1

def get_population(user_id):
    population_json = redis_client.hget(user_id,POPULATION )
    if population_json:
        serialized_population = json.loads(population_json)
        population = [genome_data for genome_data in serialized_population]
        return population
    else:
        return None
    
def save_best_model(user_id, model: Genome):
    
    best_models = get_best_models(user_id)
    print('best models to redis is')
    print(best_models)
    best_models.append(model)
    population_json = json.dumps([genome.to_dict(include_subclasses=True) for genome in best_models])
    #print(population_json)
    redis_client.hmset(user_id, {BEST_MODELS: population_json})
    
    return 1

def get_best_models(user_id):
    population_json = redis_client.hget(user_id,BEST_MODELS )
    if population_json:
        serialized_population = json.loads(population_json)
        population = [Genome(**genome_data) for genome_data in serialized_population]
        return population
    else:
        return []
    
def delete_best_models(user_id):
    redis_client.hdel(user_id, BEST_MODELS)

    


def set_fitness(user_id, fitness):
    #print(fitness)
    fitness_json = json.dumps(fitness.tolist())
    #print(fitness_json)
    redis_client.hmset(user_id, {FITNESS: fitness_json})
    return 1

def get_fitness(user_id):
    data_from_redis = redis_client.hget(user_id,FITNESS)
    fitness = json.loads(data_from_redis)
    #print(fitness)
    return fitness

def get_user_data(user_id):
   data_from_redis = redis_client.hget(user_id, f'{DATA_SET+str(1)}')
   data_dict = json.loads(data_from_redis)
   return ExperimentData(**data_dict)

def get_data_set(user_id,data_set_index):
   #print(user_id)
   data_from_redis = redis_client.hget(user_id, f'{DATA_SET+str(data_set_index)}')
   #print(data_from_redis)
   data_dict = json.loads(data_from_redis)
   return ExperimentData.from_dict(data_dict)
   #return ExperimentData(**data_dict)

def get_user_relaxation_time(user_id):
    experiment_data_json = redis_client.hget(user_id, f'{DATA_SET+str(1)}')
    if experiment_data_json:
        experiment_data = json.loads(experiment_data_json)
        return experiment_data.get(LOGARITHMIC_RELAXATION_TIME)
    else:
        return None
   # data_from_redis = redis_client.hgetall(user_id)
   # experiment_data_list = []
   # for key, value in data_from_redis.items():
     #   data_dict = json.loads(value)
     #   experiment_data_list.append(ExperimentData(**data_dict))
    #return experiment_data_list

def set_project_status(user_id,status:ProjectStatus):
    redis_client.hmset(user_id, {PROJECT_STATUS: status.value})
    return 1

def get_project_status(user_id):
    #print(user_id)
    bytes_from_redis = redis_client.hget(user_id, PROJECT_STATUS)
    value_str = bytes_from_redis.decode('utf-8')
    
    project_status = ProjectStatus(value_str)
    
    return project_status

def save_project_constants(user_id, project_constants:ProjectConstants):
       #print(project_constants.to_dict())
       project_constants_json = json.dumps(project_constants.to_dict())
       redis_client.hmset(user_id, {PROJECTS_CONSTANTS: project_constants_json})
       return 1

def save_project_constants_to_redis(user_id, project_constants:ProjectConstants):
       #print(project_constants.to_dict())
       project_constants_json = json.dumps(project_constants.to_dict())
       redis_client.hmset(user_id, {PROJECTS_CONSTANTS: project_constants_json})
       return 1


def get_project_constants_from_redis(user_id):
        data_from_redis = redis_client.hget(user_id, PROJECTS_CONSTANTS)
        if data_from_redis is None:
            return None
        return ProjectConstants.from_dict(json.loads(data_from_redis))

def get_discrepancies(user_id):
        data_from_redis = redis_client.hget(user_id, DISCREPANCY)
        if data_from_redis:
          existing_discrepancies = json.loads(data_from_redis)
        else:
          existing_discrepancies = []
       
        return existing_discrepancies

def save_discrepancies(user_id,new_discrepancies):
        existing_discrepancies = get_discrepancies(user_id)
        updated_discrepancies = existing_discrepancies + new_discrepancies
        redis_client.hmset(user_id, {DISCREPANCY: json.dumps(updated_discrepancies)})
       
        return 1

def delete_discrepancies(user_id):
       redis_client.hdel(user_id, DISCREPANCY)
       
       return 1

