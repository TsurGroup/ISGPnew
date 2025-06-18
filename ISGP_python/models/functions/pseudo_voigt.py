from models.functions.function import Function, FunctionParameters, FunctionType
import numpy as np

class PseudoVoigt(Function):
    height: float = 1
    mean: float = 0
    gaussian_variance: float = 1  # Width for Gaussian component
    lorentzian_variance: float = 1  # Width for Lorentzian component
    gauss_weight: float = 1   # Mixing factor

    def __init__(self, function_parameters: FunctionParameters,lorentzian_variance:float =1,gauss_weight:float = 1):
        super().__init__(func_type=FunctionType.PseudoVoigt, parameters_num=5)  # Call base class constructor
        self.height = function_parameters.peaks_height  # Initialize attribute specific to the subclass
        self.mean = function_parameters.tau_guess
        self.gaussian_variance = function_parameters.peaks_width
        self.lorentzian_variance = lorentzian_variance  # Assuming initial values for sigma and gamma are the same
        self.gauss_weight = gauss_weight  # Mixing factor f (0 <= f <= 1)????

    def get_value(self, x):
        # Convert x to a NumPy array for element-wise operations if it's not already one
        x = np.asarray(x)
        
        # Gaussian component
        gaussian_part = np.exp(-((x - self.mean) ** 2) / (self.gaussian_variance ** 2))
        
        # Lorentzian component
        lorentzian_part = 1 / (1 + ((x - self.mean) / self.lorentzian_variance) ** 2)
        
        # Pseudo-Voigt function: combine Gaussian and Lorentzian components
        result = self.height * (self.gauss_weight * gaussian_part + (1 - self.gauss_weight) * lorentzian_part)
        
        return result
      
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
          self.gaussian_variance = parameters[index]
          index = index + 1
        if(index < len(parameters)):
          self.lorentzian_variance = parameters[index]
          index = index + 1
        if(index < len(parameters)):
          self.gauss_weight = parameters[index]
          index = index + 1
        return index
     
    def _subclass_dict(self):
        return {"height": self.height, "mean": self.mean, "gaussian_variance": self.gaussian_variance,"lorentzian_variance":self.lorentzian_variance,"gauss_weight":self.gauss_weight}
     
    def to_string(self):
        return " "
    @classmethod
    def from_dict(cls, data):
        # Convert the dictionary back to the ColeCole object
        function_parameters = FunctionParameters(
            peaks_height=data["height"],
            tau_guess=data["mean"],
            peaks_width=data["gaussian_variance"]
        )
        # Use the alpha value from the database, or default to 0.7 if not provided
        lorentzian_variance = data["lorentzian_variance"]
        gauss_weight = data["gauss_weight"]
        return cls(function_parameters=function_parameters, lorentzian_variance=lorentzian_variance,gauss_weight=gauss_weight)  # Pass alpha as an argument