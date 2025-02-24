import numpy as np
from models.functions.function import Function, FunctionParameters, FunctionType

class NegativePseudoDelta(Function):
    height: float = 1
    mean: float = 0
    variance: float = 1
    
    def __init__(self, function_parameters: FunctionParameters):

        super().__init__(func_type=FunctionType.NegativePseudoDelta, parameters_num=2)  
        
        self.height = function_parameters.peaks_height
        self.mean = function_parameters.tau_guess_pos
        self.variance = function_parameters.d_width

    def get_value(self, x):
        return self.height * np.exp(-(((x - self.mean) / self.variance) ** 2))
    
    def get_peak(self):
        return self.height
    
    def set_parameters(self, parameters, index):
        if index < len(parameters):
            self.height = parameters[index]
            index += 1
        if index < len(parameters):
            self.mean = parameters[index]
            index += 1
        return index
    
    def _subclass_dict(self):
        return {"height": self.height, "mean": self.mean, "variance": self.variance}
    
    def to_string(self):
        if self.mean > 0:
            return f"{round(self.height, 5)}e^{{(t-{round(self.mean, 5)})^2}}"
        if self.mean < 0:
            return f"{round(self.height, 5)}e^{{(t+{-round(self.mean, 5)})^2}}"
        return f"{round(self.height, 5)}e^{{t^2}}"


    @classmethod
    def from_dict(cls, data):
        # Convert the dictionary back to the PseudoDelta object
        function_parameters = FunctionParameters(
            peaks_height=data["height"],
            tau_guess=data["mean"],
            peaks_width=data["variance"]/0.4911   # Assuming "variance" is equivalent to "peaks_width"
        )
        return cls(function_parameters=function_parameters)