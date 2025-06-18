from models.functions.function import Function, FunctionParameters, FunctionType
import numpy as np

class PearsonVII(Function):
     height: float = 1
     mean: float = 0
     variance: float = 1
     lorentz_factor:float = 1 
     
     def __init__(self, function_parameters: FunctionParameters,lorentz_factor: float = 1):
        super().__init__(func_type=FunctionType.PearsonVII, parameters_num = 4)  # Call base class constructor
        self.height = function_parameters.peaks_height  # Initialize attribute specific to the subclass
        self.mean = function_parameters.tau_guess
        self.variance = function_parameters.peaks_width
        self.lorentz_factor = lorentz_factor

     def get_value(self,x):
        return self.height / ((1 + (2 * x * np.sqrt(2**(1/self.lorentz_factor) - 1) / self.variance)**2)**self.lorentz_factor)
      
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
        if(index < len(parameters)):
          self.lorentz_factor = parameters[index]
          index = index + 1
        return index
     
     def _subclass_dict(self):
        return {"height": self.height, "mean": self.mean, "variance": self.variance,"lorentz_factor":self.lorentz_factor}
     
     def to_string(self):
        if self.mean > 0:
           return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t-{round(self.mean, 5)}}}{{{abs(round(self.alpha, 5))}}})^2}}"
        if self.mean < 0:
            return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t+{-round(self.mean, 5)}}}{{{abs(round(self.alpha, 5))}}})^2}}"   
        return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t}}{{{abs(round(self.alpha, 5))}}})^2}}" 
     
     @classmethod
     def from_dict(cls, data):
        # Convert the dictionary back to the ColeCole object
        function_parameters = FunctionParameters(
            peaks_height=data["height"],
            tau_guess=data["mean"],
            peaks_width=data["variance"]   # Assuming "variance" is equivalent to "peaks_width"
        )
        # Use the alpha value from the database, or default to 0.7 if not provided
        lorentz_factor = data["lorentz_factor"]
        return cls(function_parameters=function_parameters, lorentz_factor=lorentz_factor)  # Pass alpha as an argument