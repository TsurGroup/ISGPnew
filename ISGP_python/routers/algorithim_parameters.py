from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from project_context import get_current_project_name
from cache.cache import  get_experiment_data
from mappers.experiment_data_mapper import get_experiment_data_view
from models.project import AlgorithmParametersView
from modules.algorithim_parameters_module.algorithim_parameters_module import get_algorithm_parameters, set_algorithim_parameters
from user_context import get_current_user

router = APIRouter()



@router.get("/getExperimentData")
def getExperimentData(project_name: str = Depends(get_current_project_name)):
     
   data_set1 = get_experiment_data(0)
   data_set2 = get_experiment_data(1) 
   print(data_set2.frequency)
   print(data_set1.frequency)
   experiment_data = get_experiment_data_view(data_set1,data_set2)
    
   return experiment_data


@router.get("/getAlgorithmParameters")
def getAlgorithmParameters(project_name: str = Depends(get_current_project_name)):

   algorithim_parameters_view = get_algorithm_parameters()
   

   return algorithim_parameters_view


@router.post("/saveAlgorithmParameters")
def saveAlgorithimParameters(algorithim_parameters: AlgorithmParametersView,project_name: str = Depends(get_current_project_name)):#,session_id: str = Depends(get_current_user)
     
     #print("hey i was able to get here")
     print(algorithim_parameters)
     #print(session_id)

     set_algorithim_parameters(algorithim_parameters)

    
     return algorithim_parameters