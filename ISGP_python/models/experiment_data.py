import json
from typing import List
import numpy as np

# class ExperimentData(BaseModel):
#     frequency: List[float] = []
#     logarithmic_relaxation_time: List[float] = []
#     real_impedance: List[float] = []
#     imaginary_impedance: List[float] = []

class ExperimentData:
    def __init__(self, frequency: np.ndarray = None, logarithmic_relaxation_time: np.ndarray = None, real_impedance: np.ndarray = None, imaginary_impedance: np.ndarray = None):
        self.frequency = frequency if frequency is not None else np.array([], dtype=float)
        self.logarithmic_relaxation_time = logarithmic_relaxation_time if logarithmic_relaxation_time is not None else np.array([], dtype=float)
        self.real_impedance = real_impedance if real_impedance is not None else np.array([], dtype=float)
        self.imaginary_impedance = imaginary_impedance if imaginary_impedance is not None else np.array([], dtype=float)

    def to_dict(self):
        return {
            'frequency': self.frequency.tolist(),
            'logarithmic_relaxation_time': self.logarithmic_relaxation_time.tolist(),
            'real_impedance': self.real_impedance.tolist(),
            'imaginary_impedance': self.imaginary_impedance.tolist(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            frequency=np.array(data.get('frequency', []), dtype=float),
            logarithmic_relaxation_time=np.array(data.get('logarithmic_relaxation_time', []), dtype=float),
            real_impedance=np.array(data.get('real_impedance', []), dtype=float),
            imaginary_impedance=np.array(data.get('imaginary_impedance', []), dtype=float)
        )



# class PointData(BaseModel):
#     xValue: float = 0
#     y1Value: float = 0
#     y2Value: float = 0


# class ExperimentDataView(BaseModel):
#     realImpedance: list[PointData] = []
#     imaginaryImpedance: list[PointData] = []

#     def __init__(self, experiment_data1: ExperimentData, experiment_data2: ExperimentData):
#         super().__init__()  # Call the constructor of the BaseModel
#         self.realImpedance = []  # Initialize realImpedance as an empty list
#         self.imaginaryImpedance = []  # Initialize imaginaryImpedance as an empty list

#         for i in range(len(experiment_data1.frequency)):
#             real_impedance = PointData()
#             real_impedance.xValue = np.log10(experiment_data1.frequency[i])
#             real_impedance.y1Value = experiment_data1.real_impedance[i]
#             real_impedance.y2Value = experiment_data2.real_impedance[i]
#             self.realImpedance.append(real_impedance)

#             imaginary_impedance = PointData()
#             imaginary_impedance.xValue = np.log10(experiment_data1.frequency[i])
#             imaginary_impedance.y1Value = -experiment_data1.imaginary_impedance[i]
#             imaginary_impedance.y2Value = -experiment_data2.imaginary_impedance[i]
#             self.imaginaryImpedance.append(imaginary_impedance)