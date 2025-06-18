from models.functions.function import Function, FunctionParameters, FunctionType


class Lorentzian(Function):
     height: float = 1
     mean: float = 0
     variance: float = 1 
     
     def __init__(self, function_parameters: FunctionParameters):
        super().__init__(func_type=FunctionType.Lorentzian, parameters_num = 3)  # Call base class constructor
        self.height = function_parameters.peaks_height  # Initialize attribute specific to the subclass
        self.mean = function_parameters.tau_guess
        self.variance = function_parameters.peaks_width

     def get_value(self,x):
        return self.height/(1+((x-self.mean)/self.variance)**2)
    
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
           return f"\\frac{{{round(self.height, 5)}}}{{1+(\\frac{{t-{round(self.mean, 5)}}}{{{abs(round(self.variance, 5))}}})^2}}"
        if self.mean < 0:
            return f"\\frac{{{round(self.height, 5)}}}{{1+(\\frac{{t+{-round(self.mean, 5)}}}{{{abs(round(self.variance, 5))}}})^2}}"   
        return f"\\frac{{{round(self.height, 5)}}}{{1+(\\frac{{t}}{{{abs(round(self.variance, 5))}}})^2}}" 
     

     @classmethod
     def from_dict(cls, data):
        # Convert the dictionary back to the PseudoDelta object
        function_parameters = FunctionParameters(
            peaks_height=data["height"],
            tau_guess=data["mean"],
            peaks_width=data["variance"]  # Assuming "variance" is equivalent to "peaks_width"
        )
        return cls(function_parameters=function_parameters)
