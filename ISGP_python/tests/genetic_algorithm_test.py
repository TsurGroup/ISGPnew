import sys
import os

# # Add root to sys.path for module imports
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.genetic_algorithm.genetic_algorithm import generate_population, run_evolution


def generate_population_test():
   population =  generate_population()
   print(population)

def generate_evolution_test():
   for data in run_evolution():
             print(data.json())




