from models.functions.function import Function, FunctionParameters, FunctionType
import numpy as np

class ColeCole(Function):
     height: float = 1
     mean: float = 0
     alpha: float = 0.7 
     
     def __init__(self, function_parameters: FunctionParameters):
        super().__init__(func_type=FunctionType.ColeCole, parameters_num = 3)  # Call base class constructor
        self.height = function_parameters.peaks_height  # Initialize attribute specific to the subclass
        self.mean = function_parameters.tau_guess
        self.alpha = 0.7

     def get_value(self,x):
        return (self.height*np.sin((1-self.alpha)*np.pi))/(np.cosh(self.alpha*(x-self.mean))-np.cos((1-self.alpha)*np.pi))
    
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
        return index
     
     def _subclass_dict(self):
        return {"height": self.height, "mean": self.mean, "alpha": self.alpha}
     
     def to_string(self):
        if self.mean > 0:
           return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t-{round(self.mean, 5)}}}{{{abs(round(self.alpha, 5))}}})^2}}"
        if self.mean < 0:
            return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t+{-round(self.mean, 5)}}}{{{abs(round(self.alpha, 5))}}})^2}}"   
        return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t}}{{{abs(round(self.alpha, 5))}}})^2}}" 
