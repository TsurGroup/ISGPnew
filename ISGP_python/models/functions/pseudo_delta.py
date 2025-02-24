import numpy as np
from models.functions.function import Function, FunctionParameters, FunctionType

class PseudoDelta(Function):
    height: float = 1
    mean: float = 0
    variance: float = 1
    
    def __init__(self, function_parameters: FunctionParameters):
        # Call the base class constructor
        super().__init__(func_type=FunctionType.PseudoDelta, parameters_num=2)  # Set func_type to PsuedoDelta
        
        # Initialize the attributes specific to this class
        self.height = function_parameters.peaks_height
        self.mean = function_parameters.tau_guess
        self.variance = function_parameters.d_width

    def get_value(self, x):
        # Return the value based on the height, mean, and variance
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


     # def __init__(self, param_input):
    #     # Call base class constructor with FunctionType.PsuedoDelta
    #     super().__init__(func_type=FunctionType.PsuedoDelta, parameters_num=2)
        
    #     if isinstance(param_input, FunctionParameters):
    #         # Initialize the attributes using FunctionParameters if it's an instance
    #         self.height = param_input.peaks_height
    #         self.mean = param_input.tau_guess
    #         self.variance = param_input.d_width
    #     elif isinstance(param_input, dict):
    #         # Initialize the attributes from the dictionary
    #         self.height = param_input.get("height", self.height)  # Default to 1 if not provided
    #         self.mean = param_input.get("mean", self.mean)  # Default to 0 if not provided
    #         self.variance = param_input.get("variance", self.variance)  # Default to 1 if not provided
    #     else:
    #         raise TypeError("param_input must be either a FunctionParameters instance or a dictionary")