from models.functions.function import Function, FunctionParameters, FunctionType
import numpy as np

class HavriliakNegami(Function):
     height: float = 1
     mean: float = 0
     alpha: float = 0.6
     gamma:float = 1 
     
     def __init__(self, function_parameters: FunctionParameters):
        super().__init__(func_type=FunctionType.HavriliakNegami, parameters_num = 4)  # Call base class constructor
        self.height = function_parameters.peaks_height  # Initialize attribute specific to the subclass
        self.mean = function_parameters.tau_guess
        self.alpha = 0.6
        self.gamma = 1

     def get_value(self,x):
        value = (self.height * 10**(x * (self.alpha * self.gamma)) * np.sin(self.gamma * np.arctan(np.abs(np.sin(self.alpha * np.pi) / (10**(x * self.alpha) + np.cos(self.alpha * np.pi))))))
        value /= (100**(x * self.alpha) + np.cos(self.alpha * np.pi) * 2 * 10**(x * self.alpha) + 1)**(self.gamma / 2)
        return  value
      
     def get_peak(self):
       return self.height
     
     def set_parameters(self,parameters,index):
        if(index < len(parameters)):
          self.height = parameters[index]
          index = index + 1
        if(index < len(parameters)):
          self.mean = parameters[index]
          index = index + 1
        if(index < len(parameters)):
          self.alpha = parameters[index]
          index = index + 1
        if(index < len(parameters)):
          self.gamma = parameters[index]
          index = index + 1
        return index
     
     def _subclass_dict(self):
        return {"height": self.height, "mean": self.mean, "alpha": self.alpha,"gamma":self.gamma}
     
     def to_string(self):
        # if self.mean > 0:
        #    return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t-{round(self.mean, 5)}}}{{{abs(round(self.alpha, 5))}}})^2}}"
        # if self.mean < 0:
        #     return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t+{-round(self.mean, 5)}}}{{{abs(round(self.alpha, 5))}}})^2}}"   
        # return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t}}{{{abs(round(self.alpha, 5))}}})^2}}" 
        return ""
