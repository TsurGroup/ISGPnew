from models.functions.function import Function, FunctionParameters, FunctionType
import numpy as np

class KirkwoodFuoss(Function):
     height: float = 1
     mean: float = 0
     alpha: float  # Now alpha is dynamic, no longer hardcoded

     def __init__(self, function_parameters: FunctionParameters, alpha: float = 0.7):
        super().__init__(func_type=FunctionType.KirkwoodFuoss, parameters_num=3)  # Call base class constructor
        self.height = function_parameters.peaks_height  # Initialize attribute specific to the subclass
        self.mean = function_parameters.tau_guess
        self.alpha = alpha  # Set alpha dynamically based on input

     def get_value(self, x):
        return (self.height * np.cos((self.alpha * np.pi) / 2) * np.cos(self.alpha * (x - self.mean))) / (
            np.cos((self.alpha * np.pi) / 2) ** 2 + np.sinh(self.alpha * (x - self.mean))
        )

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
        # Convert the dictionary back to the KirkwoodFuoss object
        function_parameters = FunctionParameters(
            peaks_height=data["height"],
            tau_guess=data["mean"],
            peaks_width=data["variance"]  # Assuming "variance" is equivalent to "peaks_width"
        )
        # Use the alpha value from the database, or default to 0.7 if not provided
        alpha = data.get("alpha", 0.7)
        return cls(function_parameters=function_parameters, alpha=alpha)  # Pass alpha as an argument
