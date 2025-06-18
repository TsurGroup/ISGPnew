from models.functions.function import Function, FunctionParameters, FunctionType
import numpy as np

class ColeCole(Function):
     height: float = 1
     mean: float = 0
     alpha: float = 0.7 

     def __init__(self, function_parameters: FunctionParameters, alpha: float = 0.7):
        super().__init__(func_type=FunctionType.ColeCole, parameters_num=3)
        self.height = function_parameters.peaks_height
        self.mean = function_parameters.tau_guess
        self.alpha = alpha # Use the alpha passed from the database

     def get_value(self, x):
        return (self.height * np.sin((1 - self.alpha) * np.pi)) / (np.cosh(self.alpha * (x - self.mean)) - np.cos((1 - self.alpha) * np.pi))

     def get_peak(self):
       return self.height

     def set_parameters(self, parameters, index):
        attributes = ['height', 'mean', 'alpha']
        for i, attr in enumerate(attributes):
            if index < len(parameters):
                setattr(self, attr, parameters[index])
                index += 1
        return index

     def _subclass_dict(self):
        return {"height": self.height, "mean": self.mean, "alpha": self.alpha}

     def to_string(self):
        abs_alpha = abs(round(self.alpha, 5))  # Get the absolute value for alpha
        if self.mean > 0:
            return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t-{round(self.mean, 5)}}}{{{abs_alpha}}})^2}}"
        if self.mean < 0:
            return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t+{-round(self.mean, 5)}}}{{{abs_alpha}}})^2}}"
        return f"\\frac{{{round(self.height, 5)}}}{{cosh(\\frac{{t}}{{{abs_alpha}}})^2}}"

     @classmethod
     def from_dict(cls, data):
        # Convert the dictionary back to the ColeCole object
        function_parameters = FunctionParameters(
            peaks_height=data["height"],
            tau_guess=data["mean"],
            peaks_width=0# / 0.4911  # Assuming "variance" is equivalent to "peaks_width"
        )
        # Use the alpha value from the database, or default to 0.7 if not provided
        alpha = data["alpha"]
        return cls(function_parameters=function_parameters, alpha=alpha)  # Pass alpha as an argument
