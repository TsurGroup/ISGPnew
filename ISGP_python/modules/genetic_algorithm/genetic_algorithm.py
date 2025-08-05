import time
import numpy as np
from data_base.genomes import save_genomes
from models.project import AlgorithmParameters
from modules.output.excel_handler import save_metadata, save_run_to_excel
from cache.cache import add_discrepancies, delete_discrepancies, get_algorithm_parameters_from_cache, get_experiment_data, get_project_constants_from_cache, get_project_status, set_project_status

from decorators.timer_decorator import timer_func

from mappers.dashboard_mapper import get_dashboard_view, get_empty_dashboard_view
from models.experiment_data import ExperimentData
from models.genome import Genome
from models.project_data import ProjectConstants, ProjectStatus

from modules.genetic_algorithm.fitness import fitness
from modules.genetic_algorithm.genome_parameters import new_function,get_genome_parameters
from models.functions.function import  FunctionType

from multiprocessing import Pool

def generate_genome(experiment_data: ExperimentData,algorithm_parameters:AlgorithmParameters,project_constants:ProjectConstants,functions_num):

    genome = Genome()
    for i in range(0, functions_num):
         random_number = np.random.randint(1, 3)
         function = new_function(FunctionType(random_number),project_constants.parameters)
         genome.add_function(function)

    genome = get_genome_parameters(genome,experiment_data,algorithm_parameters,project_constants)
    #genome.fitness = fitness(genome, user_id)#need fix
    genome.fitness = fitness(genome,experiment_data,algorithm_parameters,project_constants)
    return genome

#@timer_func
def generate_genome_new(experiment_data: ExperimentData,algorithm_parameters:AlgorithmParameters,project_constants:ProjectConstants, function_type):
    #print(user_id)
    genome = Genome()  # Create a new Genome instance
    #print('function_type is:')
    #print(function_type)
    function = new_function(FunctionType(function_type), project_constants.parameters)  # Create a new function based on the FunctionType and parameters
    genome.add_function(function)  # Add the function to the genome

    genome = get_genome_parameters(genome,experiment_data,algorithm_parameters,project_constants)
    genome.fitness = fitness(genome,experiment_data,algorithm_parameters,project_constants)
    #genome.fitness = fitness(genome, user_id)#need fix

    return genome


def generate_genome_pool(experiment_data: ExperimentData, project_constants: ProjectConstants) -> list[Genome]:
    genome_pool: list[Genome] = []
    algorithm_parameters = get_algorithm_parameters_from_cache()

    # Use multiprocessing.Pool for parallel execution
    with Pool() as pool:
        # Map the initial functions to the generate_genome_new calls
        results = pool.starmap(generate_genome_new, [(experiment_data, algorithm_parameters, project_constants,value) for value in algorithm_parameters.initial_functions])
        
        # Collect the results in the genome pool
        genome_pool.extend(results)
    
    return genome_pool

#@timer_func
def generate_population():

  population:list[Genome] = []

  experiment_data = get_experiment_data(0)
  project_constants = get_project_constants_from_cache()
  algorithm_parameters = get_algorithm_parameters_from_cache()
  genome_pool = generate_genome_pool(experiment_data,project_constants)


  population = (np.random.choice(genome_pool, algorithm_parameters.population_size)).tolist()

  #set_population(user_id,population)

  return population

def mutate(genome:Genome, mutation_options,project_constants:ProjectConstants):

    function_type = np.random.choice(mutation_options)
    #print("len(genome.functions)")
    #print(len(genome.functions))
    index = np.random.randint(0, len(genome.functions))
    function = new_function(function_type,project_constants.parameters)

    new_genome = Genome()
    new_genome.functions = genome.functions.copy()
    new_genome.functions[index] = function

    return new_genome

def add_function(genome:Genome, mutation_options,project_constants:ProjectConstants):
    function_type = np.random.choice(mutation_options)
    function = new_function(function_type, project_constants.parameters)

    new_genome = Genome()
    new_genome.functions = genome.functions.copy()
    new_genome.functions.append(function)
    return new_genome

def remove_function(genome:Genome, mutation_options,project_constants:ProjectConstants):
    
    if(len(genome.functions) == 1):
        random = np.random.rand()
        if random<= 0.5:
            return add_function(genome,mutation_options,project_constants)
        else:
            return mutate(genome,mutation_options,project_constants)
    else:
        new_genome = Genome()
        remove = np.random.randint(0, len(genome.functions) - 1)
        new_genome.functions = genome.functions[:remove] + genome.functions[remove + 1:]
    return new_genome
#@timer_func
#def modify_genome(genome, genome_type_counter, algorithm_parameters: AlgorithmParameters, project_constants, experiment_data): # duplication factor code
def modify_genome(genome, algorithm_parameters: AlgorithmParameters, project_constants, experiment_data):
    new_genome = Genome()
    random = np.random.rand()

    if random <= algorithm_parameters.add_probability:
        new_genome = mutate(genome, algorithm_parameters.mutation_functions, project_constants)
    elif random <= (algorithm_parameters.mutate_probability + algorithm_parameters.add_probability):
        new_genome = add_function(genome, algorithm_parameters.mutation_functions, project_constants)
    else:
        new_genome = remove_function(genome, algorithm_parameters.mutation_functions, project_constants)

    #func_types_key = new_genome.get_func_types_key()# duplication factor code
    #unique_key = tuple(sorted(func_types_key.items()))# duplication factor code
    # Create a local counter to return
    #local_counter = genome_type_counter.copy()# duplication factor code

    #if unique_key not in local_counter:# duplication factor code
    #    local_counter[unique_key] = 1# duplication factor code
   # else:# duplication factor code
    #    local_counter[unique_key] += 1# duplication factor code

    # Check if the count exceeds the limit
    #if local_counter[unique_key] > algorithm_parameters.duplication_factor:# duplication factor code
      #  return None, local_counter# duplication factor code

    new_genome = get_genome_parameters(new_genome, experiment_data, algorithm_parameters, project_constants)
    new_genome.fitness = fitness(new_genome, experiment_data, algorithm_parameters, project_constants)

    #return new_genome, local_counter # duplication factor code
    return new_genome

def modify_genome_wrapper(args):
    #(i, population, genome_type_counter, algorithm_parameters, project_constants, experiment_data) = args  # duplication factor code
    #new_genome, updated_counter = modify_genome(population[i], genome_type_counter, algorithm_parameters, project_constants, experiment_data) # duplication factor code
    (i, population, algorithm_parameters, project_constants, experiment_data) = args
    #new_genome, updated_counter = modify_genome(population[i], algorithm_parameters, project_constants, experiment_data) # duplication factor code
    new_genome = modify_genome(population[i], algorithm_parameters, project_constants, experiment_data)
   # return new_genome, updated_counter # duplication factor code
    return new_genome


#def run_generation(population: list[Genome], genome_type_counter): # duplication factor code
def run_generation(population: list[Genome]):
    #print('pop len is')
    #print(len(population))
    
    algorithm_parameters = get_algorithm_parameters_from_cache()
    experiment_data = get_experiment_data(0)
    project_constants = get_project_constants_from_cache()
    project_status = get_project_status()

    new_population: list[Genome] = []
    
    with Pool() as pool:
       # modify_genome_args = [(i, population, genome_type_counter, algorithm_parameters, project_constants, experiment_data) for i in range(1, len(population))] # duplication factor code
        modify_genome_args = [(i, population, algorithm_parameters, project_constants, experiment_data) for i in range(1, len(population))]
        modify_genome_tasks = [pool.apply_async(modify_genome_wrapper, (args,)) for args in modify_genome_args]
        generate_genome_task = pool.apply_async(generate_genome, (experiment_data, algorithm_parameters, project_constants, algorithm_parameters.expected_peaks_num + 1))

        for task in modify_genome_tasks:
            if project_status == ProjectStatus.Aborted:
                pool.terminate()
                print("Evolution process aborted")
                set_project_status(ProjectStatus.Finished)
                return None
            #new_genome, updated_counter = task.get()# duplication factor code
            new_genome = task.get() 
            if new_genome is None:
                continue
            new_population.append(new_genome)

            # Update the genome_type_counter with the results from the worker
            #for key, value in updated_counter.items(): # duplication factor code
              #  if key in genome_type_counter: # duplication factor code
               #     genome_type_counter[key] += value # duplication factor code
              #  else: # duplication factor code
               #     genome_type_counter[key] = value # duplication factor code

        if project_status != ProjectStatus.Aborted:
            last_genome = generate_genome_task.get()

    all_population = population + new_population
    all_population.sort(key=lambda x: x.fitness, reverse=True)
    best_population = all_population[:algorithm_parameters.population_size]
    best_population[len(best_population) - 1] = last_genome

    return best_population


def run_evolution():

    algorithm_parameters = get_algorithm_parameters_from_cache()

    for i in range(algorithm_parameters.runs_num):
        #genome_type_counter = {} # duplication factor code
        delete_discrepancies()
        population = generate_population()

        #start_time = time.time()
       # for genome in population: # duplication factor code
    # Get the Counter of function types
           #func_types_key = genome.get_func_types_key() # duplication factor code
          # unique_key = tuple(sorted(func_types_key.items())) # duplication factor code

           #if unique_key not in genome_type_counter: # duplication factor code
          #   genome_type_counter[unique_key] = 0 # duplication factor code
          # genome_type_counter[unique_key] += 1 # duplication factor code
        #print("pop is:")
        #print(population)
        #end_time = time.time()
        #print(f"Operation took {end_time - start_time:.6f} seconds")

        #print("genome_type_counter is:")
        #print(genome_type_counter)
        best_genome = population[0]  # Initial best genome
        stagnant_generations = 0  # Tracks generations without improvement

        for j in range(algorithm_parameters.max_generations):

           #population = run_generation(population,genome_type_counter) # duplication factor code
            population = run_generation(population) 
            if population is None:
                return
            # print("genome_type_counter is:")
            # print(genome_type_counter)
            # Check if the best genome has changed
            current_best_genome = population[0]  # Assuming the first genome is the best
            if best_genome.id != current_best_genome.id:  # Or compare generation_created
                best_genome = current_best_genome
                stagnant_generations = 0  # Reset the count
            else:
                stagnant_generations += 1

            if stagnant_generations >= algorithm_parameters.stop_criteria:
                print(f"Run {i + 1}: No improvement for stop_criteria generations. Moving to the next run.")
                break  # Exit the current run loop

       
            
            save_genomes(i+1,j+1,population)
            
            yield get_dashboard_view(i+1, j+1, population[0])

        save_run_to_excel(i,population[0])
        if(i + 1 < algorithm_parameters.runs_num):
            
            yield get_empty_dashboard_view(i+1)
    save_metadata()
    return 1


