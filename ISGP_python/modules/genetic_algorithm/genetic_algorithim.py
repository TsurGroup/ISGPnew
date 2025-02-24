from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import math
from decorators.timer_decorator import timer_func
from models.experiment_data import ExperimentData

from models.genome import Genome
from modules.genetic_algorithm.fitness import fitness
from modules.genetic_algorithm.genome_parameters import  get_genome_parameters, new_function, simpson_matrix
from models.functions.function import  FunctionParameters, FunctionType

from redis_orm.redis_client import get_data_set, get_function_parameters, get_population, set_fitness, set_function_parameters, set_population
from user_context import current_user_id
from memory_profiler import profile
from multiprocessing import Pool, cpu_count

def generate_genome(parameters,experiment_data: ExperimentData,functions_num):
    genome = Genome()
    for i in range(0, functions_num): 
         random_number = np.random.randint(1, 3)
         function = new_function(FunctionType(random_number),parameters) 
         genome.add_function(function)

    genome = get_genome_parameters(genome,experiment_data.logarithmic_relaxation_time,experiment_data.real_impedance,experiment_data.imaginary_impedance)  
    return genome

@timer_func
#@profile
def generate_genome_pool(parameters,experiment_data):
  genome_pool :list[Genome] = [] 
  
  for i in range(1, 4): 
         genome = Genome()
         function = new_function(FunctionType(i),parameters) 
         genome.add_function(function)
         genome = get_genome_parameters(genome,experiment_data.logarithmic_relaxation_time,experiment_data.real_impedance,experiment_data.imaginary_impedance)
         genome_pool.append(genome)

  return genome_pool
@timer_func
def generate_genome_new(parameters, experiment_data, function_type):
    genome = Genome()  # Create a new Genome instance
    function = new_function(FunctionType(function_type), parameters)  # Create a new function based on the FunctionType and parameters
    genome.add_function(function)  # Add the function to the genome
    
    # Update the genome with parameters from the experimental data
    genome = get_genome_parameters(
        genome,
        experiment_data.logarithmic_relaxation_time,
        experiment_data.real_impedance,
        experiment_data.imaginary_impedance
    )
    
    return genome
@timer_func
#@profile
def generate_genome_pool_with_parallelism(parameters,experiment_data):
  genome_pool :list[Genome] = [] 
  
  with ThreadPoolExecutor() as executor:
        # Create futures for each task
        futures = [executor.submit(generate_genome_new, parameters, experiment_data, i) for i in range(1, 4)]
        # As each future completes, add its result to the genome pool
        for future in as_completed(futures):
            genome_pool.append(future.result())
  return genome_pool


@timer_func
#@profile
def generate_population():
  user_id = current_user_id.get()
  population:list[Genome] = []

  experiment_data = get_data_set(user_id,1)

  peaks_height = (-0.1)*min(experiment_data.imaginary_impedance) #redis
  peaks_width = (experiment_data.logarithmic_relaxation_time[0]-experiment_data.logarithmic_relaxation_time[-1])/len(experiment_data.logarithmic_relaxation_time) #redis
  tau_max =  math.ceil(experiment_data.logarithmic_relaxation_time[0]) #redis
  tau_min = -math.ceil(-experiment_data.logarithmic_relaxation_time[-1]) #redis

  parameters = FunctionParameters(peaks_height,peaks_width,tau_max,tau_min)
  set_function_parameters(user_id,parameters)
  
  genome_pool = generate_genome_pool_with_parallelism(parameters,experiment_data)

  population = (np.random.choice(genome_pool, 20)).tolist()
  print(population)
#     random_number = np.random.randint(1, 3)
#   for i in range(0, 20):  
#     genome = generate_genome(parameters,experiment_data,1)
#     population.append(genome)

  set_population(user_id,population) 

  return population



# def select_genome(population,population_fitness):
#    population_fitness = np.array(population_fitness)
#    #print(population_fitness)
#    #print(np.sum(population_fitness))
#    cumulative_probabilities = np.cumsum(population_fitness / np.sum(population_fitness))
   
#    random = np.random.rand()
#    indexs = np.where(cumulative_probabilities > random)[0]
#    print('picked genome index is' + str(indexs[0]))
#    return population[indexs[0]]
   
 
def mutate(genome:Genome, mutation_options,parameters:FunctionParameters):
    
    function_type = np.random.choice(mutation_options)
    index = np.random.randint(0, len(genome.functions))
    function = new_function(function_type,parameters)

    new_genome = Genome()
    new_genome.functions = genome.functions.copy()
    new_genome.functions[index] = function
    
    return new_genome

def add_function(genome:Genome, mutation_options,parameters:FunctionParameters):
    function_type = np.random.choice(mutation_options)
    function = new_function(function_type, parameters)

    new_genome = Genome()
    new_genome.functions = genome.functions.copy()
    new_genome.functions.append(function) 
    return new_genome  

def remove_function(genome:Genome, mutation_options,parameters:FunctionParameters):
    
    if(len(genome.functions) == 1):
        random = np.random.rand()
        if random<= 0.5:
            return add_function(genome,mutation_options,parameters)
        else:
            return mutate(genome,mutation_options,parameters)
    else:
        new_genome = Genome()
        remove = np.random.randint(0, len(genome.functions) - 1)
        new_genome.functions = genome.functions[:remove] + genome.functions[remove + 1:]
    return new_genome

# def process_wrapper(i,genome,mutatation_probability, addition_probability, mutation_options, parameters, experiment_data):
#     return modify_genome(genome, mutatation_probability, addition_probability, mutation_options, parameters, experiment_data)

#@check_stop_factory(user_id=current_user_id.get())
#@check_stop
#@profile
def modify_genome(genome,mutatation_probability,addition_probability,mutation_options,parameters,experiment_data):
        new_genome =  Genome()
        random = np.random.rand()
        user_id = current_user_id.get()
        #print('random is: '+ str(random))

        if random <= mutatation_probability:
           new_genome = mutate(genome,mutation_options,parameters)

        elif random <= (mutatation_probability + addition_probability):
           #print('im adding a function')
           new_genome = add_function(genome,mutation_options,parameters)

        else:
           new_genome = remove_function(genome,mutation_options,parameters)

        new_genome = get_genome_parameters(new_genome,experiment_data.logarithmic_relaxation_time,experiment_data.real_impedance,experiment_data.imaginary_impedance)

        new_genome.fitness = fitness(new_genome, user_id)
        return new_genome

def modify_genome_wrapper(args):
    index, population, mutation_probability, addition_probability, mutation_options, parameters, experiment_data = args
    return modify_genome(population[index], mutation_probability, addition_probability, mutation_options, parameters, experiment_data)

@timer_func
def run_generation_with_parallelism(population, population_fitness, experiment_data, parameters):
    user_id = current_user_id.get()
    mutation_options = [1, 2, 3]
    mutation_probability = 0.5
    addition_probability = 0.25

    new_population = []
    num_cpus = cpu_count()
    #print(f"Number of CPUs available: {num_cpus}")
    with Pool() as pool:
        # Prepare arguments for modify_genome_wrapper
        modify_genome_args = [(i, population, mutation_probability, addition_probability, mutation_options, parameters, experiment_data) for i in range(1, 20)]
        
        # Submit modify_genome tasks to the pool
        modify_genome_tasks = [pool.apply_async(modify_genome_wrapper, (args,)) for args in modify_genome_args]
        
        # Submit generate_genome task to the pool
        generate_genome_task = pool.apply_async(generate_genome, (parameters, experiment_data, 4))

        # Collect results from modify_genome tasks
        for task in modify_genome_tasks:
            new_genome = task.get()
            if new_genome is None:
                return None, None
            new_population.append(new_genome)

        # Collect result from generate_genome task
        last_genome = generate_genome_task.get()


    print('new_population at begining  is: ')
    print(new_population)


    new_population_fitness = np.array([fitness(genome, user_id) for genome in new_population])

    all_fitnesses = np.concatenate((population_fitness, new_population_fitness))
    print('fitnesses are: ' + str(all_fitnesses))
    all_population = population + new_population

    top_20_indices = np.argsort(all_fitnesses)[-20:][::-1]
    population_fitness = all_fitnesses[top_20_indices]
    best_population = [all_population[i] for i in top_20_indices]

    # Place the last genome in the last position of the best population
    best_population[19] = last_genome
    print('best_population at end is: ')
    print(best_population)
    
    print('peaks num:')
    peaks_num = np.array([len(genome.functions) for genome in best_population])
    print(peaks_num)

    return best_population, population_fitness


@timer_func
#@profile
def run_generation(population,population_fitness,experiment_data,parameters):
     user_id = current_user_id.get()
     mutation_options =  [1,2,3]
     mutatation_probability = 0.5
     addition_probability = 0.25

     new_population:list[Genome] = []
     
     for i in range(0, 20): 
        new_genome =  Genome()
        genome  = population[i]
        #print('user id prior to modify_genome is:' + str(user_id))
        new_genome = modify_genome(genome,mutatation_probability,addition_probability,mutation_options,parameters,experiment_data)
        if (new_genome is None):
            return None,None
        new_population.append(new_genome)
     
     new_population_fitness = np.array([fitness(genome,user_id) for genome in new_population])    #i should add to parallel bt adding to genome
     
     all_fitnesses = np.concatenate((population_fitness, new_population_fitness))
     #print(all_fitnesses)
     all_population = population + new_population

     top_20_indices = np.argsort(all_fitnesses)[-20:][::-1]
     population_fitness = all_fitnesses[top_20_indices]
     best_population = [all_population[i] for i in top_20_indices]

    
     last_genome = generate_genome(parameters,experiment_data,4)
     best_population[19] = last_genome
     

     return best_population,population_fitness


def run_evolution():
     user_id = current_user_id.get()
     #print(type(user_id))
     
     population = generate_population()
     experiment_data = get_data_set(user_id,0)
     parameters = get_function_parameters(user_id)
     #print(population)
     population_fitness = np.array([fitness(genome, user_id) for genome in population])
     
     for i in range(0, 10): 
      #population,population_fitness = run_generation(population,population_fitness,experiment_data,parameters)
      population,population_fitness = run_generation_with_parallelism(population,population_fitness,experiment_data,parameters)

      if (population is None or population_fitness is None):
         return
      #print(population)
      set_population(user_id,population)
      set_fitness(user_id,population_fitness)

      point_difference = 3
      point = (experiment_data.logarithmic_relaxation_time[0] - experiment_data.logarithmic_relaxation_time[1])/point_difference
      tt  = np.arange(-20, 20, point)
      imag , real = simpson_matrix(population[0].get_genome_value(tt),np.array(experiment_data.logarithmic_relaxation_time),point)
      
    #   yield get_impadence_graph_view(i,population_fitness[0],
    #                                  experiment_data.real_impedance,experiment_data.imaginary_impedance,
    #                                  experiment_data.real_impedance,experiment_data.imaginary_impedance,
    #                                  real,imag)
     
     return get_population(user_id)

        


  

## select_pair
## crossover

##  mutation


