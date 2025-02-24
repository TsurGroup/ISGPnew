from collections import Counter
import json
import uuid
import numpy as np
from pydantic import BaseModel
from models.functions.function import Function

class Genome(BaseModel):
   id: str = uuid.uuid4().hex
   functions : list[Function] =[]
   fitness: float = 0
   discrepancy:float = 0
   area_penalty:float = 0 
   peakes_width_penalty:float = 0
   peakes_num_penalty:float = 0
   free_parameters_penalty:float = 0
   compatibility_penalty:float = 0

   @property
   def new_fitness(self):
        return self.area_penalty * self.peakes_width_penalty* self.peakes_num_penalty* self.free_parameters_penalty* self.compatibility_penalty

   def add_function(self, function):
        self.functions.append(function)

   def get_func_types_key(self) -> Counter:
        """Return a Counter of the function types for this genome."""
        return Counter(func.func_type for func in self.functions)  
   
   def get_parameters_num(self):
       parameters_num = 0
       for function in self.functions:
           parameters_num = parameters_num + function.parameters_num
       return parameters_num
   
   def get_genome_value(self,x):

       value = np.zeros(len(x))
       for function in self.functions:
        #print(function)
       # print(len(x))
        value = value + function.get_value(x)
       return value
   
   def get_genome_peaks_width(self):
       max = 0
       for function in self.functions:
           if(function.func_type <=2 and max < function.variance):
               max = function.variance
       return max
   
   def get_area(self,x,hh):
       area = 0
       for function in self.functions:
           area = area + abs(np.trapz(function.get_value(x), dx=hh))
       return area
   
   def set_parameters(self,parameters):
       i = 0
       function_num = 0
       while(i < len(parameters)):
           i = self.functions[function_num].set_parameters(parameters,i)
           function_num = function_num + 1
       return i
   
   def to_dict(self, include_subclasses=True):
        data = self.dict()
        if include_subclasses:
            data["functions"] = [func.dict() for func in self.functions]
        return data
   
   def get_latex_string(self):
        latex_string =  " + ".join(func.to_string() for func in self.functions)
        return f"$f(t) = {latex_string}$"
   

   def to_dict(self):
       return {
           "fitness": self.fitness,
           "discrepancy": self.discrepancy,
           "area_penalty": self.area_penalty,
           "peakes_width_penalty": self.peakes_width_penalty,
           "peakes_num_penalty": self.peakes_num_penalty,
           "free_parameters_penalty": self.free_parameters_penalty,
           "compatibility_penalty": self.compatibility_penalty,
           "functions": json.dumps([func.dict() for func in self.functions])  # Serialize functions
       }

#    @classmethod
#    def from_dict(cls, data):
#        functions_data = json.loads(data['functions'])
#        functions = [Function(**func) for func in functions_data]
#        return cls(
#            functions=functions,
#            fitness=data['fitness'],
#            discrepancy=data['discrepancy'],
#            area_penalty=data['area_penalty'],
#            peakes_width_penalty=data['peakes_width_penalty'],
#            peakes_num_penalty=data['peakes_num_penalty'],
#            free_parameters_penalty=data['free_parameters_penalty'],
#            compatibility_penalty=data['compatibility_penalty']
#       )