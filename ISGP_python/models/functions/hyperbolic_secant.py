
import warnings
from models.functions.function import Function, FunctionParameters, FunctionType
import numpy as np

class HyperbolicSecant(Function):
     height: float = 1
     mean: float = 0
     variance: float = 1 
     
     def __init__(self, function_parameters: FunctionParameters):
        super().__init__(func_type=FunctionType.HyperbolicSecant, parameters_num = 3)  # Call base class constructor
        self.height = function_parameters.peaks_height  # Initialize attribute specific to the subclass
        self.mean = function_parameters.tau_guess
        self.variance = function_parameters.peaks_width

     def get_value(self,x):
         arg = (x - self.mean) / self.variance

        # Catch warnings as they happen
         with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", RuntimeWarning)  # Capture all runtime warnings
            
            result = self.height / np.cosh(arg)
            
            # Check if any RuntimeWarning was triggered
            for warning in w:
                if issubclass(warning.category, RuntimeWarning):
                    print(f"Overflow encountered in np.cosh for x={x}, mean={self.mean}, variance={self.variance}, arg={arg}")
        
         return result # Or another appropriate fallback value
         return self.height/np.cosh((x-self.mean)/self.variance)
    
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
          self.variance = parameters[index]
          index = index + 1
        return index
     
     def _subclass_dict(self):
        return {"height": self.height, "mean": self.mean, "variance": self.variance}
     
     def to_string(self):
        if self.mean > 0:
           return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t-{round(self.mean, 5)}}}{{{abs(round(self.variance, 5))}}})^2}}"
        if self.mean < 0:
            return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t+{-round(self.mean, 5)}}}{{{abs(round(self.variance, 5))}}})^2}}"   
        return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t}}{{{abs(round(self.variance, 5))}}})^2}}" 
