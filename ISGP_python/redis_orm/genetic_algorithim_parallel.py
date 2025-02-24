# from concurrent.futures import ThreadPoolExecutor, as_completed
# import numpy as np
# from decorators.timer_decorator import timer_func
# from evolution_status_context import get_abort_flag, get_evolution_running
# from mappers.dashboard_mapper import get_dashboard_view
# from models.experiment_data import ExperimentData
# ##from models.project_data import ProjectConstants, ProjectStatus
# ##from models.view_models.view_models import get_dashboard_view
# from models.genome import Genome
# from models.project_data import ProjectConstants, ProjectStatus
# from modules.experiment_data_module.constant_data import get_project_constants

# from modules.genetic_algorithm.fitness import fitness
# from modules.genetic_algorithm.genome_parameters import  get_genome_parameters, new_function
# from models.functions.function import  FunctionType
# from redis_orm.redis_client import delete_best_models, delete_discrepancies, get_best_models, get_data_set, get_population, get_project_status, save_best_model, save_discrepancies, set_population, set_project_status
# from user_context import current_user_id
# from multiprocessing import Pool

# def generate_genome(experiment_data: ExperimentData,project_constants:ProjectConstants,functions_num):
    
#     genome = Genome()
#     for i in range(0, functions_num): 
#          random_number = np.random.randint(1, 3)
#          function = new_function(FunctionType(random_number),project_constants.parameters) 
#          genome.add_function(function)

#     genome = get_genome_parameters(genome,experiment_data,project_constants)
#     #genome.fitness = fitness(genome, user_id)#need fix
#     genome.fitness = fitness(genome,experiment_data,project_constants)
#     return genome


# #@timer_func
# def generate_genome_new(user_id,experiment_data: ExperimentData,project_constants:ProjectConstants, function_type):   
#     print(user_id)
#     genome = Genome()  # Create a new Genome instance
#     function = new_function(FunctionType(function_type), project_constants.parameters)  # Create a new function based on the FunctionType and parameters
#     genome.add_function(function)  # Add the function to the genome

#     genome = get_genome_parameters(genome,experiment_data,project_constants)
#     genome.fitness = fitness(genome,experiment_data,project_constants)
#     #genome.fitness = fitness(genome, user_id)#need fix
    
#     return genome
# #@timer_func
# #@profile
# def generate_genome_pool_with_parallelism(user_id,experiment_data: ExperimentData,project_constants:ProjectConstants):
#   genome_pool :list[Genome] = [] 
  
#   with ThreadPoolExecutor() as executor:
#         # Create futures for each task
#         futures = [executor.submit(generate_genome_new, user_id,experiment_data,project_constants, i) for i in range(1, 4)]
#         # As each future completes, add its result to the genome pool
#         for future in as_completed(futures):
#             genome_pool.append(future.result())
#   return genome_pool


# #@timer_func
# def generate_population():
#   user_id = current_user_id.get()
#   population:list[Genome] = []

#   experiment_data = get_data_set(user_id,0)
#   project_constants = get_project_constants()  
#   genome_pool = generate_genome_pool_with_parallelism(user_id,experiment_data,project_constants)

#   #population = (np.random.choice(genome_pool, 20)).tolist()
#   population = (np.random.choice(genome_pool, 20)).tolist()
  
#   set_population(user_id,population) 

#   return population

# def mutate(genome:Genome, mutation_options,project_constants:ProjectConstants):
    
#     function_type = np.random.choice(mutation_options)
#     index = np.random.randint(0, len(genome.functions))
#     function = new_function(function_type,project_constants.parameters)

#     new_genome = Genome()
#     new_genome.functions = genome.functions.copy()
#     new_genome.functions[index] = function
    
#     return new_genome

# def add_function(genome:Genome, mutation_options,project_constants:ProjectConstants):
#     function_type = np.random.choice(mutation_options)
#     function = new_function(function_type, project_constants.parameters)

#     new_genome = Genome()
#     new_genome.functions = genome.functions.copy()
#     new_genome.functions.append(function) 
#     return new_genome  

# def remove_function(genome:Genome, mutation_options,project_constants:ProjectConstants):
    
#     if(len(genome.functions) == 1):
#         random = np.random.rand()
#         if random<= 0.5:
#             return add_function(genome,mutation_options,project_constants)
#         else:
#             return mutate(genome,mutation_options,project_constants)
#     else:
#         new_genome = Genome()
#         remove = np.random.randint(0, len(genome.functions) - 1)
#         new_genome.functions = genome.functions[:remove] + genome.functions[remove + 1:]
#     return new_genome

# def modify_genome(user_id,genome,mutatation_probability,addition_probability,mutation_options,project_constants,experiment_data):
#         new_genome =  Genome()
#         random = np.random.rand()
        
#        # print('random is: '+ str(random))

#         if random <= addition_probability:
#            new_genome = mutate(genome,mutation_options,project_constants)

#         elif random <= (mutatation_probability + addition_probability):
#           # print('im adding a function')
#            new_genome = add_function(genome,mutation_options,project_constants)
#           # print(new_genome)
#           # print(len(new_genome.functions))
#         else:
#            new_genome = remove_function(genome,mutation_options,project_constants)

#         new_genome = get_genome_parameters(new_genome,experiment_data,project_constants)
#         new_genome.fitness = fitness(new_genome,experiment_data,project_constants)
#         return new_genome

# def modify_genome_wrapper(args):
#     index, user_id, population, mutation_probability, addition_probability, mutation_options, project_constants, experiment_data = args
#     return modify_genome(user_id,population[index], mutation_probability, addition_probability, mutation_options, project_constants, experiment_data)

# def run_generation_with_parallelism(population):
#     user_id = current_user_id.get()
#     mutation_options = [1, 2, 3]
#     mutation_probability = 0.5
#     addition_probability = 0.25

#     experiment_data = get_data_set(user_id, 0)
#     project_constants = get_project_constants()

#     # abort_flag = get_abort_flag()
#     # evolution_running = get_evolution_running()
#     project_status = get_project_status(user_id)

#     new_population = []
#     with Pool() as pool:
#         modify_genome_args = [(i, user_id, population, mutation_probability, addition_probability, mutation_options, project_constants, experiment_data) for i in range(1, len(population))]
#         modify_genome_tasks = [pool.apply_async(modify_genome_wrapper, (args,)) for args in modify_genome_args]
#         generate_genome_task = pool.apply_async(generate_genome, (experiment_data, project_constants, 4))

#         for task in modify_genome_tasks:
#             if project_status == ProjectStatus.Aborted:
#                 pool.terminate()
#                 print("Evolution process aborted")
#                 set_project_status(user_id,ProjectStatus.Finished)
#                 return None
#             new_genome = task.get()
#             if new_genome is None:
#                 continue
#             #print('new genome after taks is done is:')
#             #print(len(new_genome.functions))
#             new_population.append(new_genome)

#         if project_status != ProjectStatus.Aborted:
#             last_genome = generate_genome_task.get()

#     if project_status == ProjectStatus.Aborted:
#         print("Evolution process aborted")
#         set_project_status(user_id,ProjectStatus.Finished)
#         return None

#     all_population = population + new_population
#     all_population.sort(key=lambda x: x.fitness, reverse=True)
    
#     # for model in all_population:
#     #     print('area is: ' + str(model.fitness))
#     best_population = all_population[:20]
   
#     best_population[len(best_population)-1] = last_genome
    
#     peaks_num_all = np.array([len(genome.functions) for genome in all_population])
#     print('Peaks num of best:', peaks_num_all)


#     peaks_num = np.array([len(genome.functions) for genome in best_population])
#     #print('Peaks num of best:', peaks_num)

#     return best_population


# def run_evolution_with_parallesim():
#      user_id = current_user_id.get()
#      #print(type(user_id))
#      delete_best_models(user_id)
#      delete_discrepancies(user_id)
#      population = generate_population()
     
#      for i in range(0, 10): 
#       #population,population_fitness = run_generation(population,population_fitness,experiment_data,parameters)
#       #population = run_generation_with_parallelism(population,experiment_data,parameters)
#        population = run_generation_with_parallelism(population)
#        if (population is None):
#           return
#        save_best_model(user_id,population[0])
#        best_models = get_best_models(user_id)

#     #    for func in population[0].functions:
#     #         print(func._subclass_dict())
#     #         print(func.mean)

#        #print(best_models)
#        #discrepancies = [(genome.discrepancy,genome.get_parameters_num()) for genome in population]
#        discrepancies = [{'discrepancy':genome.discrepancy,'parameters_num':genome.get_parameters_num()} for genome in population]
#        save_discrepancies(user_id,discrepancies)
       

#        #print(discrepancies)
#        set_population(user_id,population)
       



#        yield get_dashboard_view(user_id,i,population[0])

     
#      return get_population(user_id)

    