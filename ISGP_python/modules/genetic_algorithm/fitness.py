import math
import numpy as np
from models.project import AlgorithmParameters
from cache.cache import get_algorithm_parameters_from_cache
from models.experiment_data import ExperimentData
from models.genome import Genome
from models.project_data import ProjectConstants
from modules.genetic_algorithm.genome_parameters import  simpson_matrix

def weighted_average(sample, weight):
    if weight == 1:
        weight = 2

    if weight >= len(sample):
        return np.mean(sample)

    sample_avg = []

    num_intervals = len(sample) // weight #the floor division // rounds the result down to the nearest whole number

    for i in range(num_intervals):
        interval_average = np.mean(sample[i * weight : (i + 1) * weight])
        sample_avg.extend([interval_average] * weight)

    remaining_samples = len(sample) - num_intervals * weight
    if remaining_samples > 0:
        last_interval_average = np.mean(sample[num_intervals * weight :])
        sample_avg.extend([last_interval_average] * remaining_samples)

    return np.array(sample_avg)

#def fit(genome: Genome,user_id,data_set_id):
def fit(genome:Genome,experiment_data: ExperimentData,project_constants:ProjectConstants,alpha):
 
  #experiment_data = get_data_set(user_id,data_set_id)
  #w0 = 0.00001
  #w1 = 0.001
  #print(type(experiment_data.logarithmic_relaxation_time))
  angular_velocity = 2 * np.pi * experiment_data.frequency
  #angular_velocity = 1/(10**experiment_data.logarithmic_relaxation_time)

  function_samples = genome.get_genome_value(project_constants.time_samples)

  yi,y_r = simpson_matrix(function_samples,project_constants)

  freq = angular_velocity/(2 * np.pi)

  weight = math.floor(len(freq) / (np.log10(freq[-1] / freq[0])))
  
  real_impedance_avg = weighted_average(experiment_data.real_impedance,weight)
  imaginary_impedance_avg = weighted_average(experiment_data.imaginary_impedance,weight)
  
  #print(len(experiment_data.imaginary_impedance))
  #SSY1=(experiment_data.imaginary_impedance-imaginary_impedance_avg)*project_constants.filter
  #SSYr1=(experiment_data.real_impedance-real_impedance_avg)*project_constants.filter
  
  SSY1= experiment_data.imaginary_impedance-imaginary_impedance_avg
  SSYr1=experiment_data.real_impedance-real_impedance_avg


  if(project_constants.use_filter):
      SSY1 *= project_constants.filter
      SSYr1 *= project_constants.filter
  #print('SSY1 is: '+ str(SSY1))
  #print('SSYr1 is: '+ str(SSYr1))

  SSY = np.sqrt(np.mean(SSY1 ** 2))
  SSYr = np.sqrt(np.mean(SSYr1 ** 2))

  #SSF1=(yi-experiment_data.imaginary_impedance)*project_constants.filter
  #SSFr1=(y_r-experiment_data.real_impedance)*project_constants.filter
  
  SSF1=yi-experiment_data.imaginary_impedance
  SSFr1=y_r-experiment_data.real_impedance

  if(project_constants.use_filter):
      SSF1 *= project_constants.filter
      SSFr1 *= project_constants.filter
  
  SSF = np.sqrt(np.mean(SSF1 ** 2))
  SSFr = np.sqrt(np.mean(SSFr1 ** 2))
    
  fit1i=SSY/(SSY+SSF)
  fit1r=SSYr/(SSYr+SSFr)
  #print('fit1i is: ' + str(fit1i))
  #print('fit1r is: ' + str(fit1r))
  discrepency = np.sum(((experiment_data.real_impedance - y_r)**2 + (experiment_data.imaginary_impedance - yi)**2) / np.sqrt(y_r**2 + yi**2) * project_constants.filter)

  fit = alpha*fit1i+(1-alpha)*fit1r
  #return alpha*fit1i+(1-alpha)*fit1r
  return fit,discrepency


#def compatibility_penalty(genome:Genome,user_id):
def compatibility_penalty(genome:Genome,experiment_data: ExperimentData,project_constants:ProjectConstants,alpha):
   #fit1 = fit(genome,user_id,0)
   fit1,discrepency1 = fit(genome,experiment_data,project_constants,alpha)

   #fit2 = fit(genome,user_id,1)
   fit2,discrepency2 = fit(genome,experiment_data,project_constants,alpha)
  
   penalty1=(alpha*fit1+(1-alpha)*fit2)

   parameters_num = genome.get_parameters_num()
   discrepency = (alpha*discrepency1+(1-alpha)*discrepency2)/(2*len(experiment_data.imaginary_impedance)-parameters_num-2)
   return penalty1,discrepency


def free_parameters_penalty(genome:Genome):
  num_of_found_peaks = len(genome.functions)
  num_of_parameters = genome.get_parameters_num()
  penalty2 = 1/(1+np.exp(num_of_parameters/num_of_found_peaks-6))
  return penalty2


def peakes_num_penalty(genome:Genome,num_of_guessed_peaks):
 num_of_found_peaks = len(genome.functions)

 #penalty3 = 1 / (1 + np.exp(2 * (num_of_found_peaks - num_of_guessed_peaks - 2.5)))
 penalty3 = 1 / (1 + np.exp(2 * (num_of_found_peaks - num_of_guessed_peaks - 2.3)))
 return penalty3

def peakes_width_penalty(genome: Genome,algorithm_parameters:AlgorithmParameters):
 sigmamax = algorithm_parameters.width_factor; ###the range of measured freq (in log scale)
 sigma = genome.get_genome_peaks_width()
 penalty4 = 1/(1 + np.exp(-7*(sigmamax-sigma)/sigmamax))
 return penalty4

#def area_penalty(genome: Genome,user_id):
def area_penalty(genome:Genome,norm_factor,project_constants:ProjectConstants):
 FitnessGauss = norm_factor

 area = genome.get_area(project_constants.time_samples,project_constants.interval)
 #print('area is: ' + str(area))
 penalty5 = 1 - FitnessGauss*(1-np.exp(-(1-area)**2))
 return penalty5


#def fitness(genome:Genome,user_id):
def fitness(genome:Genome,experiment_data: ExperimentData,algorithm_parameters:AlgorithmParameters,project_constants:ProjectConstants):
 #print('do i get here???')
 penalty1,discrepency = compatibility_penalty(genome,experiment_data,project_constants,algorithm_parameters.alpha)
 genome.compatibility_penalty = penalty1
 genome.discrepancy = discrepency

 penalty2 = free_parameters_penalty(genome)
 genome.free_parameters_penalty = penalty2
 
 penalty3 = peakes_num_penalty(genome,algorithm_parameters.expected_peaks_num)
 genome.peakes_num_penalty = penalty3

 penalty4 = peakes_width_penalty(genome,algorithm_parameters)
 genome.peakes_width_penalty = penalty4

 penalty5 = area_penalty(genome,algorithm_parameters.norm_factor,project_constants)
 genome.area_penalty = penalty5


 fitness = penalty1*penalty2*penalty3*penalty4*penalty5
 #print('individual fitnes is' + str(fitness))
 return fitness