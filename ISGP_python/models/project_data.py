from enum import Enum
import numpy as np
from models.functions.function import FunctionParameters


class ProjectStatus(Enum):
    Pending = "pending"
    Running = "running"    
    Aborted= "aborted"
    Finished= "finished"

class SigmoidFilter:
   useFilter = False
   w0:float = 0.001
   w1:float = 0.0001
   filter: np.ndarray = None

   def apply_filter(self,data):
      if self.useFilter:
        return data * self.filter
      return data




class ProjectConstants:
    def __init__(self, parameters: FunctionParameters = None, time_samples: np.ndarray = None, filter: np.ndarray = None, 
                 kernel: np.ndarray = None, c_vector: np.ndarray = None, normalization_factor: float = 1.0,interval: float = 1.0):
        self.parameters = parameters if parameters is not None else FunctionParameters()
        self.time_samples = time_samples if time_samples is not None else np.array([], dtype=float)
        self.filter = filter if filter is not None else np.array([], dtype=float)
        self.kernel = kernel if kernel is not None else np.array([], dtype=complex)  # Note: dtype is complex
        self.c_vector = c_vector if c_vector is not None else np.array([], dtype=float)
        self.normalization_factor = normalization_factor  # New float property
        self.interval = interval
        self.use_filter = False

    def to_dict(self):
        return {
            'parameters': self.parameters.to_dict(),
            'time_samples': self.time_samples.tolist(),
            'filter': self.filter.tolist(),
            'kernel_real': self.kernel.real.tolist(),  # Separate real and imaginary parts
            'kernel_imag': self.kernel.imag.tolist(),
            'c_vector': self.c_vector.tolist(),
            'normalization_factor': self.normalization_factor,  # Serialize normalization_factor
            'interval': self.interval,
        }

    @classmethod
    def from_dict(cls, data):
        # Combine real and imaginary parts to form complex numbers
        kernel_complex = np.array(data['kernel_real'], dtype=float) + 1j * np.array(data['kernel_imag'], dtype=float)
        
        return cls(
            parameters=FunctionParameters.from_dict(data['parameters']),
            time_samples=np.array(data['time_samples'], dtype=float),
            filter=np.array(data['filter'], dtype=float),
            kernel=kernel_complex,
            c_vector=np.array(data['c_vector'], dtype=float),
            normalization_factor=data.get('normalization_factor', 1.0),
            interval=data.get('interval', 1.0)  # Retrieve normalization_factor with default  # Retrieve normalization_factor with default
        )
    
    def apply_filter(self,data):
      if self.use_filter:
        return data #* self.filter
      return data

    
