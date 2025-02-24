import numpy as np
from modules.algorithim_parameters_module.algorithim_parameters_module import get_algorithm_parameters, set_algorithim_parameters
from data_base.algorithm_parameters import upsert_filter_parameters
from modules.experiment_data_module.constant_data import calculate_filter
from cache.cache import get_experiment_data, get_project_constants_from_cache, set_algorithm_parameters_cache, set_project_constants
from view_models.graph_view import PointData

def get_filtered_data(w0,w1):
    filtered_graph = []
    data_set1 = get_experiment_data(0)
    data_set2 = get_experiment_data(1)
    
    algorithm_parameters = get_algorithm_parameters()
    set_algorithim_parameters(algorithm_parameters)
    upsert_filter_parameters(w0,w1,True)
    set_algorithm_parameters_cache()

    project_constants = get_project_constants_from_cache()

    project_constants = calculate_filter(True,w0,w1,data_set1,project_constants)
    
    set_project_constants(project_constants)
    
    
    imaginary_impedance1_min = min(data_set1.imaginary_impedance) 
    imaginary_impedance2_min = min(data_set2.imaginary_impedance) 

    filtered_data = project_constants.filter#*min(imaginary_impedance1_min,imaginary_impedance2_min)
    for i in range(len(data_set1.frequency)):
            
            point = PointData()
            point.x = 2 * np.pi *data_set1.frequency[i]
            point.y = filtered_data[i]
            filtered_graph.append(point)

    return filtered_graph