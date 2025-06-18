import numpy as np
from scipy.optimize import minimize
from decorators.timer_decorator import timer_func
from models.functions import *

from models.project import AlgorithmParameters
from models.experiment_data import ExperimentData
from models.functions.function import  FunctionParameters, FunctionType
from models.genome import Genome
from models.project_data import ProjectConstants
from typing import List, Tuple

method = 0

def new_function(func_type:FunctionType,function_parameters:FunctionParameters):
    if func_type == FunctionType.PseudoDelta:
        return PseudoDelta(function_parameters)
    elif func_type == FunctionType.Gaussian:
        return Gaussian(function_parameters)
    elif func_type == FunctionType.Lorentzian:
        return Lorentzian(function_parameters)
    elif func_type == FunctionType.HyperbolicSecant:
        return HyperbolicSecant(function_parameters)
    elif func_type == FunctionType.ColeCole:
        return ColeCole(function_parameters)
    elif func_type == FunctionType.KirkwoodFuoss:
        return KirkwoodFuoss(function_parameters)
    elif func_type == FunctionType.PearsonVII:
        return PearsonVII(function_parameters)
    elif func_type == FunctionType.Losev:
        return Losev(function_parameters)
    elif func_type == FunctionType.HavriliakNegami:
        return HavriliakNegami(function_parameters)
    elif func_type == FunctionType.AsymmetricGaussian:
        return AsymmetricGaussian(function_parameters)
    elif func_type == FunctionType.AsymmetricLorentzian:
        return AsymmetricLorentzian(function_parameters)
    elif func_type == FunctionType.AsymmetricHyperbolicSecant:
        return AsymmetricHyperbolicSecant(function_parameters)
    elif func_type == FunctionType.PseudoVoigt:
        return PseudoVoigt(function_parameters)
    elif func_type == FunctionType.LeftPseudoDelta:
        return LeftPseudoDelta(function_parameters)
    elif func_type == FunctionType.RightPseudoDelta:
        return RightPseudoDelta(function_parameters)
    elif func_type == FunctionType.NegativePseudoDelta:
        return NegativePseudoDelta(function_parameters)
    elif func_type == FunctionType.NegativeGaussian:
        return NegativeGaussian(function_parameters)
    elif func_type == FunctionType.NegativeLorentzian:
        return NegativeLorentzian(function_parameters)
    elif func_type == FunctionType.NegativeHyperbolicSecant:
        return NegativeHyperbolicSecant(function_parameters)

    else:
        raise ValueError(f"Unknown function of type: {func_type}")
 
def get_initial_guess(genome: Genome, experiment_data: ExperimentData) -> float:

    logarithmic_relaxation_time = experiment_data.logarithmic_relaxation_time
    min_imaginary_impedance = -min(experiment_data.imaginary_impedance)
    random_log_relax_time = -logarithmic_relaxation_time[np.random.randint(len(logarithmic_relaxation_time))]
    log_relax_time_diff = (logarithmic_relaxation_time[-1] - logarithmic_relaxation_time[0]) / len(logarithmic_relaxation_time)

    initial_parameters = []
    
    for function in genome.functions:
        initial_parameters.extend([min_imaginary_impedance, random_log_relax_time])
        #if function.func_type == FunctionType.PsuedoDelta:
           # initial_parameters.append(-(logarithmic_relaxation_time[1] - logarithmic_relaxation_time[0]) / 10)
        if function.func_type in {FunctionType.Gaussian, FunctionType.Lorentzian, FunctionType.HyperbolicSecant,FunctionType.NegativeGaussian,FunctionType.NegativeLorentzian,FunctionType.NegativeHyperbolicSecant}:
            initial_parameters.append(log_relax_time_diff)
        elif function.func_type in {FunctionType.ColeCole, FunctionType.KirkwoodFuoss}:
            initial_parameters.append(np.random.rand())
        elif function.func_type == FunctionType.PearsonVII:
            initial_parameters.extend([log_relax_time_diff, 1])
        elif function.func_type in {FunctionType.Losev, FunctionType.AsymmetricGaussian, FunctionType.AsymmetricLorentzian, FunctionType.AsymmetricHyperbolicSecant}:
            initial_parameters.extend([log_relax_time_diff, log_relax_time_diff])
        elif function.func_type == FunctionType.HavriliakNegami:
            initial_parameters.extend([np.random.rand(), log_relax_time_diff])
        elif function.func_type == FunctionType.PseudoVoigt:
            initial_parameters.extend([log_relax_time_diff, log_relax_time_diff, np.random.rand()])
    
    return initial_parameters

def get_genome_bounds(genome: Genome, logarithmic_relaxation_time, algorithm_parameters: AlgorithmParameters) -> List[Tuple[float, float]]:
    sigma = (logarithmic_relaxation_time[0] - logarithmic_relaxation_time[-1]) / (2 * len(logarithmic_relaxation_time))
    bounds = []

    additional_bounds = {
        FunctionType.PseudoDelta: [],
        FunctionType.LeftPseudoDelta: [],
        FunctionType.RightPseudoDelta: [],
        FunctionType.NegativePseudoDelta: [],
        FunctionType.Gaussian: [(sigma, algorithm_parameters.width_factor)],
        FunctionType.NegativeGaussian: [(sigma, algorithm_parameters.width_factor)],
        FunctionType.Lorentzian: [(sigma, algorithm_parameters.width_factor)],
        FunctionType.NegativeLorentzian: [(sigma, algorithm_parameters.width_factor)],
        FunctionType.HyperbolicSecant: [(sigma, algorithm_parameters.width_factor)],
        FunctionType.NegativeHyperbolicSecant: [(sigma, algorithm_parameters.width_factor)],
        FunctionType.ColeCole: [(0.7, 0.9)],
        FunctionType.KirkwoodFuoss: [(0.6, 0.9)],
        FunctionType.PearsonVII: [(sigma, algorithm_parameters.width_factor), (0, 2)],
        FunctionType.Losev: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor)],
        FunctionType.HavriliakNegami: [(0.6, 1), (0.00001, 0.99999)],
        FunctionType.AsymmetricGaussian: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor)],
        FunctionType.AsymmetricLorentzian: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor)],
        FunctionType.AsymmetricHyperbolicSecant: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor)],
        FunctionType.PseudoVoigt: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor), (0, 1)]
    }

    for function in genome.functions:
        bounds.append((0, np.inf))#
        bounds.append((algorithm_parameters.lower_bounds[function.func_type], algorithm_parameters.upper_bounds[function.func_type]))
        bounds.extend(additional_bounds.get(function.func_type, []))

    return bounds

# def get_genome_parameters(genome:Genome,experiment_data: ExperimentData,algorithm_parameters:AlgorithmParameters,project_constants:ProjectConstants):
#    if method is 0:
#        return get_genome_parameters_by_parameter(genome,experiment_data,algorithm_parameters,project_constants)
#    return get_genome_parameters_by_function(genome,experiment_data,algorithm_parameters,project_constants)

def get_genome_parameters(genome:Genome,experiment_data: ExperimentData,algorithm_parameters:AlgorithmParameters,project_constants:ProjectConstants):
   updated_genome=Genome()
   if method == 0:
       updated_genome = get_genome_parameters_by_parameter(genome,experiment_data,algorithm_parameters,project_constants)
       return get_genome_parameters_by_parameter(updated_genome,experiment_data,algorithm_parameters,project_constants)
   updated_genome = get_genome_parameters_by_function(genome,experiment_data,algorithm_parameters,project_constants)
   return get_genome_parameters_by_function(updated_genome,experiment_data,algorithm_parameters,project_constants)


def get_genome_parameters_by_parameter(genome:Genome,experiment_data: ExperimentData,algorithm_parameters:AlgorithmParameters,project_constants:ProjectConstants)->Genome:
    
    parameters = get_initial_guess(genome,experiment_data)
    genome_bounds = get_genome_bounds(genome,experiment_data.logarithmic_relaxation_time,algorithm_parameters)
    parameters_num = genome.get_parameters_num()

    for i in range(0,parameters_num):
       res = minimize(function_minimum, parameters[0:i+1], bounds=genome_bounds[0:i+1], args=(genome, experiment_data, project_constants), options={'maxiter': 50})
       parameters[0:i+1] = res.x

    x0 = parameters 
    res = minimize(function_minimum, x0, bounds=genome_bounds[0:parameters_num], args=(genome, experiment_data, project_constants), options={'maxiter': 50})

    parameters = res.x
    genome.set_parameters(parameters)
    
    return genome

def get_genome_parameters_by_function(genome:Genome,experiment_data: ExperimentData,algorithm_parameters:AlgorithmParameters,project_constants:ProjectConstants)->Genome:
    
    parameters = get_initial_guess(genome,experiment_data)
    genome_bounds = get_genome_bounds(genome,experiment_data.logarithmic_relaxation_time,algorithm_parameters)
    parameters_num = 0

    for function in genome.functions:
       parameters_num = parameters_num + function.parameters_num
       res = minimize(function_minimum, parameters[0:parameters_num], bounds=genome_bounds[0:parameters_num], args=(genome, experiment_data, project_constants), options={'maxiter': 50})
       parameters[0:parameters_num] = res.x

    x0 = parameters 
    res = minimize(function_minimum, x0, bounds=genome_bounds[0:parameters_num], args=(genome, experiment_data, project_constants), options={'maxiter': 50})
    parameters = res.x
    genome.set_parameters(parameters)
    
    return genome

#@timer_func
def function_minimum(x0, genome:Genome, experiment_data:ExperimentData, project_constants:ProjectConstants):
  
  genome.set_parameters(x0)

  samples = genome.get_genome_value(project_constants.time_samples)
  imag , real = simpson_matrix(samples,project_constants)

  ea1 = experiment_data.real_impedance-real
  ea2 = experiment_data.imaginary_impedance-imag
  
  if(project_constants.use_filter):
      ea1 *= project_constants.filter
      ea2 *= project_constants.filter
  #ea1 = project_constants.apply_filter(experiment_data.real_impedance-real)
  #ea2 = project_constants.apply_filter(experiment_data.imaginary_impedance-imag)

  ea = np.vstack((ea1, ea2))
  ea_flat = ea.flatten()

  return ea_flat.T @ ea_flat

#@timer_func
def simpson_matrix(samples,project_constants:ProjectConstants):
   scalars = samples[:, np.newaxis] 

   convolution_matrix = project_constants.kernel * scalars
   Imp1 = np.dot(convolution_matrix.T, project_constants.c_vector)

   imag = np.imag(Imp1)  # Flatten to convert to 1D array
   real = np.real(Imp1)

   return imag , real



# def guess(parameters: list[float], genome: Genome, experiment_data: ExperimentData) -> float:
#     # Calculate values that don't depend on the loop
#     logarithmic_relaxation_time = experiment_data.logarithmic_relaxation_time
#     min_imaginary_impedance = -min(experiment_data.imaginary_impedance)
#     random_log_relax_time = -logarithmic_relaxation_time[np.random.randint(len(logarithmic_relaxation_time))]
#     log_relax_time_diff = (logarithmic_relaxation_time[-1] - logarithmic_relaxation_time[0]) / len(logarithmic_relaxation_time)
    
#     # Initialize the parameter list
#     initial_parameters = []
    
#     # Iterate over each function in the genome
#     for function in genome.functions:
#         # Add common parameters for each function
#         initial_parameters.append(min_imaginary_impedance)
#         initial_parameters.append(random_log_relax_time)
        
#         # Add function-specific parameters
#        # if function.func_type == FunctionType.PsuedoDelta:
#            # initial_parameters.append(-(logarithmic_relaxation_time[1] - logarithmic_relaxation_time[0]) / 10)
#         if function.func_type in {FunctionType.Gaussian, FunctionType.Lorentzian, FunctionType.HyperbolicSecant}:
#             initial_parameters.append(log_relax_time_diff)
#         elif function.func_type in {FunctionType.ColeCole, FunctionType.KirkwoodFuoss}:
#             initial_parameters.append(np.random.rand())
#         elif function.func_type == FunctionType.PearsonVII:
#             initial_parameters.extend([log_relax_time_diff, 1])
#         elif function.func_type in {FunctionType.Losev, FunctionType.AsymmetricGaussian, FunctionType.AsymmetricLorentzian, FunctionType.AsymmetricHyperbolicSecant}:
#             initial_parameters.extend([log_relax_time_diff, log_relax_time_diff])
#         elif function.func_type == FunctionType.HavriliakNegami:
#             initial_parameters.extend([np.random.rand(), log_relax_time_diff])
#         elif function.func_type == FunctionType.PseudoVoigt:
#             initial_parameters.extend([log_relax_time_diff, log_relax_time_diff, np.random.rand()])
    
#     print('len(parameters):')
#     print(len(parameters))
#     print(initial_parameters)
    
#     return initial_parameters[len(parameters)]

# def guess_by_function(function_type:FunctionType, experiment_data: ExperimentData) -> float:
#     # Calculate values that don't depend on the loop
#     logarithmic_relaxation_time = experiment_data.logarithmic_relaxation_time
#     min_imaginary_impedance = -min(experiment_data.imaginary_impedance)
#     random_log_relax_time = -logarithmic_relaxation_time[np.random.randint(len(logarithmic_relaxation_time))]
#     log_relax_time_diff = (logarithmic_relaxation_time[-1] - logarithmic_relaxation_time[0]) / len(logarithmic_relaxation_time)
    
#     # Initialize parameters with common initial values
#     initial_parameters = [min_imaginary_impedance, random_log_relax_time]
    
#     # Add function-specific parameters
 
#     if function_type == FunctionType.PsuedoDelta:
#             initial_parameters.append(-(logarithmic_relaxation_time[1] - logarithmic_relaxation_time[0]) / 10)
#     elif function_type in {FunctionType.Gaussian, FunctionType.Lorentzian, FunctionType.HyperbolicSecant}:
#             initial_parameters.append(log_relax_time_diff)
#     elif function_type in {FunctionType.ColeCole, FunctionType.KirkwoodFuoss}:
#             initial_parameters.append(np.random.rand())
#     elif function_type == FunctionType.PearsonVII:
#             initial_parameters.extend([log_relax_time_diff, 1])
#     elif function_type in {FunctionType.Losev, FunctionType.AsymmetricGaussian, FunctionType.AsymmetricLorentzian, FunctionType.AsymmetricHyperbolicSecant}:
#             initial_parameters.extend([log_relax_time_diff, log_relax_time_diff])
#     elif function_type == FunctionType.HavriliakNegami:
#             initial_parameters.extend([np.random.rand(), log_relax_time_diff])
#     elif function_type == FunctionType.PseudoVoigt:
#             initial_parameters.extend([log_relax_time_diff, log_relax_time_diff, np.random.rand()])
    
#     return initial_parameters

# def get_parameters_bounds(parameters: list[float], genome: Genome, logarithmic_relaxation_time, algorithm_parameters: AlgorithmParameters) -> List[Tuple[float, float]]:
#     sigma = (logarithmic_relaxation_time[0] - logarithmic_relaxation_time[-1]) / (2 * len(logarithmic_relaxation_time))
#     bounds = []
    
#     # Define a dictionary for additional bounds based on function type
#     additional_bounds = {
#         FunctionType.PsuedoDelta: [],
#         FunctionType.Gaussian: [(sigma, algorithm_parameters.width_factor)],
#         FunctionType.Lorentzian: [(sigma, algorithm_parameters.width_factor)],
#         FunctionType.HyperbolicSecant: [(sigma, algorithm_parameters.width_factor)],
#         FunctionType.ColeCole: [(0.7, 0.9)],
#         FunctionType.KirkwoodFuoss: [(0.6, 0.9)],
#         FunctionType.PearsonVII: [(sigma, algorithm_parameters.width_factor), (0, 2)],
#         FunctionType.Losev: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor)],
#         FunctionType.HavriliakNegami: [(0.6, 1), (0.00001, 0.99999)],
#         FunctionType.AsymmetricGaussian: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor)],
#         FunctionType.AsymmetricLorentzian: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor)],
#         FunctionType.AsymmetricHyperbolicSecant: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor)],
#         FunctionType.PseudoVoigt: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor), (0, 1)]
#     }
    
#     # Append the bounds for each function
#     for function in genome.functions:
#         # Add the common (0, np.inf) and (lower_bounds, upper_bounds) bounds, then specific function bounds
#         bounds.append((0, np.inf))
#         bounds.append((algorithm_parameters.lower_bounds[function.func_type], algorithm_parameters.upper_bounds[function.func_type]))
#         bounds.extend(additional_bounds.get(function.func_type, []))
    
#     # Ensure bounds are trimmed to the length of parameters
#     return bounds[:len(parameters)]


# def get_function_bounds(function_type:FunctionType, logarithmic_relaxation_time, algorithm_parameters: AlgorithmParameters) -> List[Tuple[float, float]]:
#     sigma = (logarithmic_relaxation_time[0] - logarithmic_relaxation_time[-1]) / (2 * len(logarithmic_relaxation_time))
#     bounds = []
    
#     # Define a dictionary for additional bounds based on function type
#     additional_bounds = {
#         FunctionType.PsuedoDelta: [],
#         FunctionType.Gaussian: [(sigma, algorithm_parameters.width_factor)],
#         FunctionType.Lorentzian: [(sigma, algorithm_parameters.width_factor)],
#         FunctionType.HyperbolicSecant: [(sigma, algorithm_parameters.width_factor)],
#         FunctionType.ColeCole: [(0.7, 0.9)],
#         FunctionType.KirkwoodFuoss: [(0.6, 0.9)],
#         FunctionType.PearsonVII: [(sigma, algorithm_parameters.width_factor), (0, 2)],
#         FunctionType.Losev: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor)],
#         FunctionType.HavriliakNegami: [(0.6, 1), (0.00001, 0.99999)],
#         FunctionType.AsymmetricGaussian: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor)],
#         FunctionType.AsymmetricLorentzian: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor)],
#         FunctionType.AsymmetricHyperbolicSecant: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor)],
#         FunctionType.PseudoVoigt: [(sigma, algorithm_parameters.width_factor), (sigma, algorithm_parameters.width_factor), (0, 1)]
#     }
    
 
#     bounds.append((0, np.inf))
#     bounds.append((algorithm_parameters.lower_bounds[function_type], algorithm_parameters.upper_bounds[function_type]))
#     bounds.extend(additional_bounds.get(function_type, []))
    
#     # Ensure bounds are trimmed to the length of parameters
#     return bounds

#@timer_func
#def get_genome_parameters(genome:Genome,frequency,real_impedance,imaginary_impedance):
# def get_genome_parameters(genome:Genome,experiment_data: ExperimentData,algorithm_parameters:AlgorithmParameters,project_constants:ProjectConstants)->Genome:
    
#     parameters_num = genome.get_parameters_num()
#     #print(genome)
#     print('parameters_num is :'+ str(parameters_num))

#     #options = {'maxiter': 50}
#     parameters = []

#     for i in range(0,parameters_num):
#        #np.append(parameters, a)
       
#        #a = guess(parameters,genome,frequency,imaginary_impedance)
#        a = guess(parameters,genome,experiment_data)
#        #print(a)
#        parameters = np.append(parameters, a)

#        bounds = get_parameters_bounds(parameters,genome,experiment_data.logarithmic_relaxation_time,algorithm_parameters)
#        #res = minimize(function_minimum, parameters, bounds=list(zip([-7],[1.2] )), args=(genome, frequency, real_impedance, imaginary_impedance), options=options)
#        res = minimize(function_minimum, parameters, bounds=bounds, args=(genome, experiment_data, project_constants), options={'maxiter': 50})

#        parameters = res.x
#        #print('parameters after optimization is: '+ str(parameters))

#     x0 = parameters 
#     #print(bounds)
#     #res = minimize(function_minimum, x0, bounds=list(zip([-7],[1.2] )), args=(genome, frequency, real_impedance, imaginary_impedance), options=options)
#     res = minimize(function_minimum, x0, bounds=bounds, args=(genome, experiment_data, project_constants), options={'maxiter': 50})

#     parameters = res.x
#     genome.set_parameters(parameters)
    
#     return genome