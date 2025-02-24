import math
import numpy as np
#from cache.cache import get_project_constants_from_cache, set_project_constants
from models.experiment_data import ExperimentData
from models.functions.function import FunctionParameters
from models.project_data import ProjectConstants
#from redis_orm.redis_client import get_project_constants_from_redis, save_project_constants_to_redis

from user_context import current_user_id

def calculate_constant_data(experiment_data_1: ExperimentData,experiment_data_2: ExperimentData): #seperate into smaller functions
    
    project_constants = ProjectConstants()
    
    project_constants.normalization_factor = experiment_data_1.real_impedance[-1]+0.2*experiment_data_2.real_impedance[-1]

    peaks_height = (-0.1)*min(experiment_data_1.imaginary_impedance) 
    peaks_width = (experiment_data_1.logarithmic_relaxation_time[0]-experiment_data_1.logarithmic_relaxation_time[-1])/len(experiment_data_1.logarithmic_relaxation_time)
    tau_max =  math.ceil(experiment_data_1.logarithmic_relaxation_time[0]) 
    tau_min = -math.ceil(-experiment_data_1.logarithmic_relaxation_time[-1]) 
    
    tau_guess=(tau_max-tau_min)/2-tau_max
    tau_guess_pos=0
     
    pos_tau = np.where(experiment_data_1.logarithmic_relaxation_time > 0, 1, 0)  # Equivalent to u(y>0)
    pos_tau = -np.ceil(-pos_tau[-1])  # Taking the last element
    #tau_guess = (pos_tau - tau_min) / 2 - pos_tau
    tau_guess_pos = (tau_max - pos_tau) / 2 - tau_max

    # if False:   
    #  pos_tau = np.where(experiment_data_1.logarithmic_relaxation_time > 0, 1, 0)  # Equivalent to u(y>0)
    #  pos_tau = -np.ceil(-pos_tau[-1])  # Taking the last element
    #  tau_guess = (pos_tau - tau_min) / 2 - pos_tau
    #  tau_guess_pos = (tau_max - pos_tau) / 2 - tau_max
    
    #project_constants.parameters = FunctionParameters(peaks_height,peaks_width,tau_max,tau_min)
    project_constants.parameters = FunctionParameters(peaks_height,peaks_width,tau_guess,tau_guess_pos)
    #print(project_constants.parameters.to_dict())

    return project_constants

def calculate_filter(use_filter,w0:float,w1:float,experiment_data_1: ExperimentData,project_constants: ProjectConstants): #seperate into smaller functions
    
    project_constants.use_filter = use_filter
    angular_velocity = 1/(10**experiment_data_1.logarithmic_relaxation_time)

    project_constants.filter = 1 / (1 + np.exp(-5 * np.log10(angular_velocity / w0) / np.log10(w1 / w0)))

    return project_constants
   

def calculate_time_intervals(experiment_data: ExperimentData, project_constants: ProjectConstants,point_difference):
  
    project_constants.interval =  -(experiment_data.logarithmic_relaxation_time[1]-experiment_data.logarithmic_relaxation_time[0])/point_difference
    
    project_constants.time_samples = np.arange(-20, 20, project_constants.interval)
    

    angular_velocity = 1/(10**experiment_data.logarithmic_relaxation_time)
    project_constants.kernel = 1 / (1 + 1j * ((np.power(10, project_constants.time_samples)).reshape(-1, 1) * angular_velocity))

    c = np.ones(project_constants.time_samples.size)
    c[1::2] = 4  # Modify every second line starting from the second line to be 4
    c[2::2] = 2    # Modify every second line starting from the third line to be 2
    c = c * (project_constants.interval / point_difference)

    project_constants.c_vector = c

    return project_constants







    