from pydantic import BaseModel
import numpy as np
from enum import IntEnum


class FunctionType(IntEnum):
    PseudoDelta = (0, "Pseudo Delta","General")
    Gaussian = (1, "Gaussian","General")
    Lorentzian = (2, "Lorentzian","General")
    HyperbolicSecant = (3, "Hyperbolic Secant","General")
    ColeCole = (4, "Cole-Cole","General")
    KirkwoodFuoss = (5, "Kirkwood-Fuoss","General")
    PearsonVII = (6, "Pearson VII","General")
    Losev = (7, "Losev","General")
    HavriliakNegami = (8, "Havriliak-Negami","General")
    AsymmetricGaussian = (9, "Asymmetric Gaussian","General")
    AsymmetricLorentzian = (10, "Asymmetric Lorentzian","General")
    AsymmetricHyperbolicSecant = (11, "Asymmetric Hyperbolic Secant","General")
    PseudoVoigt = (12, "Pseudo Voigt","General")

    LeftPseudoDelta = (13, "Left Psuedo Delta","OutOfBounds")
    RightPseudoDelta = (14, "Right Psuedo Delta","OutOfBounds")

    NegativePseudoDelta = (15, "Negative Pseudo Delta","Negative")
    NegativeGaussian = (16, "Negative Gaussian","Negative")
    NegativeLorentzian = (17, "Negative Lorentzian","Negative")
    NegativeHyperbolicSecant = (18, "Negative Hyperbolic Secant","Negative")
    NewForTest = (19, "NewForTest","Negative")
    
    
    def __new__(cls, value, description, category):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        obj.category = category
        return obj
    
    def __str__(self):
        return self.description  # Only return the description


class FunctionParameters:

    def __init__(self, peaks_height: float = 1, peaks_width: float = 0, tau_guess: float = 1, tau_guess_pos: float = 0):
        self.peaks_height = peaks_height
        self.peaks_width = peaks_width
        self.tau_guess = tau_guess
        self.tau_guess_pos = tau_guess_pos

    @property
    def d_width(self):
        return 0.4911 * self.peaks_width

    def to_dict(self):
        return {
            'peaks_height': self.peaks_height,
            'peaks_width': self.peaks_width,
            'tau_guess': self.tau_guess,
            'tau_guess_pos': self.tau_guess_pos
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            peaks_height=data.get('peaks_height', 1),
            peaks_width=data.get('peaks_width', 0),
            tau_guess=data.get('tau_guess', 1),
            tau_guess_pos=data.get('tau_guess_pos', 0)
        )

class Function(BaseModel):
    func_type: FunctionType
    parameters_num: int

    def get_value(self, x):
        return np.array([])

    def get_peak(self):
        return []

    def set_parameters(self, parameters, index):
        return 0

    def get_area(self, x, hh):
        return abs(np.trapz(self.get_value(x), dx=hh))

    @classmethod
    def from_dict(cls, data):
        # Create an instance based on the function type
        func_type = FunctionType(data["func_type"])  # Convert the value back to FunctionType
        if func_type == FunctionType.PseudoDelta:
            from models.functions.pseudo_delta import PseudoDelta  # Import subclass dynamically
            return PseudoDelta.from_dict(data)
        elif func_type == FunctionType.Gaussian:
            from models.functions.gaussian import Gaussian  # Import subclass dynamically
            return Gaussian.from_dict(data)
        elif func_type == FunctionType.Lorentzian:
            from models.functions.lorentzian import Lorentzian  # Import subclass dynamically
            return Lorentzian.from_dict(data)
        elif func_type == FunctionType.HyperbolicSecant:
            from models.functions.hyperbolic_secant import HyperbolicSecant  # Import subclass dynamically
            return HyperbolicSecant.from_dict(data)
        elif func_type == FunctionType.ColeCole:
            from models.functions.cole_cole import ColeCole  # Import subclass dynamically
            return ColeCole.from_dict(data)
        elif func_type == FunctionType.KirkwoodFuoss:
            from models.functions.kirkwood_fuoss import KirkwoodFuoss  # Import subclass dynamically
            return KirkwoodFuoss.from_dict(data)
        elif func_type == FunctionType.PearsonVII:
            from models.functions.pearson_vii import PearsonVII  # Import subclass dynamically
            return PearsonVII.from_dict(data)
        elif func_type == FunctionType.Losev:
            from models.functions.losev import Losev  # Import subclass dynamically
            return Losev.from_dict(data)
        elif func_type == FunctionType.PseudoVoigt:
            from models.functions.pseudo_voigt import PseudoVoigt  # Import subclass dynamically
            return PseudoVoigt.from_dict(data)
        elif func_type == FunctionType.AsymmetricGaussian:
            from models.functions.asymmetric_gaussian import AsymmetricGaussian  # Import subclass dynamically
            return AsymmetricGaussian.from_dict(data)
        elif func_type == FunctionType.AsymmetricLorentzian:
            from models.functions.asymmetric_lorentzian import AsymmetricLorentzian  # Import subclass dynamically
            return AsymmetricLorentzian.from_dict(data)
        elif func_type == FunctionType.AsymmetricHyperbolicSecant:
            from models.functions.asymmetric_hyperbolic_secant import AsymmetricHyperbolicSecant  # Import subclass dynamically
            return AsymmetricHyperbolicSecant.from_dict(data)
       
        else:
            raise ValueError(f"Unknown function type: {func_type}")

    def to_dict(self, **kwargs):
        base_dict = super().dict(**kwargs)
        subclass_dict = self._subclass_dict()
        return {**base_dict, **subclass_dict}

    def _subclass_dict(self):
        return {}

    def to_string(self):
        return ''
    
     



