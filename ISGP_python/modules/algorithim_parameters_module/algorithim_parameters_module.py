import math
import numpy as np
from data_base.algorithm_parameters import save_algorithm_parameters_to_db
from models.functions.function import FunctionType
from cache.cache import delete_project_constants_cache, get_experiment_data, get_project_constants_from_cache, set_algorithm_parameters_cache,get_algorithm_parameters_from_cache, update_project_constants_from_cache
from mappers.algorithim_parameters_mapper import get_algorithm_parameters_from_view
from models.project import AlgorithmParameters, AlgorithmParametersView



def get_algorithm_parameters():
 
 algorithm_parameters = get_algorithm_parameters_from_cache()
 if algorithm_parameters is None:

    project_constants = get_project_constants_from_cache()
    data_set1 = get_experiment_data(0)
    data_set2 = get_experiment_data(1)
    
    tau_max = np.ceil(data_set1.logarithmic_relaxation_time[0])
    tau_min = -math.ceil(-data_set1.logarithmic_relaxation_time[-1]) 
    pos_tau = 0.8*data_set1.logarithmic_relaxation_time[0]+0.2*data_set2.logarithmic_relaxation_time[0]##not sure y is called this. u should change and call it something else


    upper_bounds = {func.value: pos_tau for func in FunctionType}## this should be the normalization factor which is the max of real impadance(kk kroning)
    lower_bounds = {func.value: tau_min for func in FunctionType}


    upper_bounds[FunctionType.NegativePseudoDelta.value] = tau_max
    upper_bounds[FunctionType.NegativeGaussian.value] = tau_max
    upper_bounds[FunctionType.NegativeLorentzian.value] = tau_max
    upper_bounds[FunctionType.NegativeHyperbolicSecant.value] = tau_max

    lower_bounds[FunctionType.NegativePseudoDelta.value] = pos_tau
    lower_bounds[FunctionType.NegativeGaussian.value] = pos_tau
    lower_bounds[FunctionType.NegativeLorentzian.value] = pos_tau
    lower_bounds[FunctionType.NegativeHyperbolicSecant.value] = pos_tau

    upper_bounds[FunctionType.LeftPseudoDelta.value] = tau_max+3
    upper_bounds[FunctionType.RightPseudoDelta.value] = tau_min-3

    lower_bounds[FunctionType.LeftPseudoDelta.value] = tau_max+1.5
    lower_bounds[FunctionType.RightPseudoDelta.value] = tau_min-4

    algorithm_parameters = AlgorithmParameters(upper_bounds=upper_bounds,lower_bounds=lower_bounds)

    algorithm_parameters.width_factor  = -(data_set1.logarithmic_relaxation_time[-1] - data_set1.logarithmic_relaxation_time[0])

    algorithm_parameters.initial_functions = [0]
    #algorithm_parameters.mutation_functions= [0,1,2,3]
    algorithm_parameters.mutation_functions= [0,1]

 return algorithm_parameters.to_view()

def set_algorithim_parameters(algorithim_parameters_view: AlgorithmParametersView):
    
 algorithm_params = AlgorithmParameters.from_view(algorithim_parameters_view)
 print(algorithm_params)
 save_algorithm_parameters_to_db(algorithm_params)


 update_project_constants_from_cache()
 #delete_project_constants_cache()
 
 return 1

