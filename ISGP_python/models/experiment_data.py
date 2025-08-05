import numpy as np


class ExperimentData:
    '''
    Model for holding frequency domain impedance experiment data.
    '''

    def __init__(self, 
                 frequency: np.ndarray = None, 
                 logarithmic_relaxation_time: np.ndarray = None, 
                 real_impedance: np.ndarray = None, 
                 imaginary_impedance: np.ndarray = None,
                 normalization_factor: float = None):
        '''
        Parameters:
        frequency [Hz]: measured frequency
        logarithmic_relaxation_time: calculated using frequency as log10(1 / frequency)
        real_impedance [Ohm]: measured real impedance (normalized internally)
        imaginary_impedance [Ohm]: measured imaginary impedance (normalized internally)
        normalization_factor: if None, automatically set to max(real_impedance)
        '''

        self.frequency = frequency if frequency is not None else np.array([], dtype=float)

        if logarithmic_relaxation_time is not None:
            self.logarithmic_relaxation_time = logarithmic_relaxation_time
        elif frequency is not None:
            self.logarithmic_relaxation_time = np.log10(1 / frequency)
        else:
            self.logarithmic_relaxation_time = np.array([], dtype=float)

        self.real_impedance = real_impedance if real_impedance is not None else np.array([], dtype=float)
        self.imaginary_impedance = imaginary_impedance if imaginary_impedance is not None else np.array([], dtype=float)

        self.normalization_factor = normalization_factor
        # Ensure all arrays are the same length
        lengths = [len(self.frequency), len(self.logarithmic_relaxation_time),
                   len(self.real_impedance), len(self.imaginary_impedance)]

        if len(set(lengths)) != 1:
            raise ValueError("All input arrays must be the same length.")

    def to_dict(self):
        return {
            'frequency': self.frequency.tolist(),
            'logarithmic_relaxation_time': self.logarithmic_relaxation_time.tolist(),
            'real_impedance': self.real_impedance.tolist(),
            'imaginary_impedance': self.imaginary_impedance.tolist(),
            'normalization_factor': self.normalization_factor
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            frequency=np.array(data.get('frequency', []), dtype=float),
            logarithmic_relaxation_time=np.array(data.get('logarithmic_relaxation_time', []), dtype=float),
            real_impedance=np.array(data.get('real_impedance', []), dtype=float),
            imaginary_impedance=np.array(data.get('imaginary_impedance', []), dtype=float),
            normalization_factor=data.get('normalization_factor')  # Can be None
        )
