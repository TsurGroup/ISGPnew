from typing import Dict, List
from pydantic import BaseModel

from models.functions.function import FunctionType

class FilterDataView(BaseModel):
    w0: float
    w1: float
    useFilter: bool


class AlgorithmParametersView(BaseModel):
    runsNum: int = 3
    maxGenerations: int = 100
    mutateProbability: float = 0.5
    addProbability: float = 0.25
    stopCriteria: int = 10
    duplicationFactor:int = 7
    
    expectedPeaksNum:int = 3
    normFactor: float = 0.05
    pointDiff: float = 3
    widthFactor: float = 8
    alpha: float = 0.8
    
    populationSize: int = 20
   
    functionTypes: list = []
    # outOfBoundsFunctionTypes: list = []
    # negativeFunctionTypes: list = []
    # forcedFunctionTypes: list = []

    initialFunctions: List[FunctionType] = []
    mutationFunctions: List[FunctionType] = []

    upperBounds: Dict[int, float] = {}
    lowerBounds: Dict[int, float] = {}

    @property
    def removeProbability(self) -> float:
        return 1 - (self.mutateProbability + self.addProbability)


class AlgorithmParameters:
    def __init__(self, runs_num=3, max_generations=100, mutate_probability=0.5, add_probability=0.25, stop_criteria=10,duplication_factor=7,
                 expected_peaks_num =3,norm_factor=0.05, point_diff=3, width_factor=8, alpha=0.8,use_filter=False, population_size=20,w0 =0.001,w1 = 0.0001,
                 initial_functions=None, mutation_functions=None, upper_bounds=None, lower_bounds=None):
        self.runs_num = runs_num
        self.max_generations = max_generations
        self.mutate_probability = mutate_probability
        self.add_probability = add_probability
        self.stop_criteria = stop_criteria
        self.duplication_factor = duplication_factor
        
        self.use_filter = use_filter
        self.w0 = w0
        self.w1 = w1
        
        self.expected_peaks_num = expected_peaks_num
        self.norm_factor = norm_factor
        self.point_diff = point_diff
        self.width_factor = width_factor
        self.alpha = alpha

        self.population_size = population_size
        self.initial_functions = initial_functions or []
        self.mutation_functions = mutation_functions or []
        self.upper_bounds = upper_bounds or {}
        self.lower_bounds = lower_bounds or {}

    @classmethod
    def from_view(cls, view: AlgorithmParametersView):
        
        return cls(
            runs_num=view.runsNum,
            max_generations=view.maxGenerations,
            mutate_probability=view.mutateProbability,
            add_probability=view.addProbability,
            stop_criteria=view.stopCriteria,
            duplication_factor = view.duplicationFactor,

            expected_peaks_num = view.expectedPeaksNum,
            norm_factor=view.normFactor,
            point_diff=view.pointDiff,
            width_factor=view.widthFactor,
            alpha=view.alpha,
            population_size=view.populationSize,
            initial_functions=view.initialFunctions,
            mutation_functions=view.mutationFunctions,
            upper_bounds={FunctionType(func): bound for func, bound in view.upperBounds.items()},
            lower_bounds={FunctionType(func): bound for func, bound in view.lowerBounds.items()}
        )

    def to_view(self) -> AlgorithmParametersView:
        return AlgorithmParametersView(
            runsNum=self.runs_num,
            maxGenerations=self.max_generations,
            mutateProbability=self.mutate_probability,
            addProbability=self.add_probability,
            stopCriteria=self.stop_criteria,
            duplicationFactor=self.duplication_factor,

            expectedPeaksNum=self.expected_peaks_num,
            normFactor=self.norm_factor,
            pointDiff=self.point_diff,
            widthFactor=self.width_factor,
            alpha=self.alpha,

            populationSize=self.population_size,
            functionTypes = [{"value": ft.value,"description": ft.description, "category": ft.category } for ft in FunctionType],
            # outOfBoundsFunctionTypes = [ft.description for ft in FunctionType],
            # negativeFunctionTypes = [ft.description for ft in FunctionType],
            # forcedFunctionTypes = [ft.description for ft in FunctionType],

            initialFunctions=self.initial_functions,
            mutationFunctions=self.mutation_functions,
            upperBounds=self.upper_bounds,
            lowerBounds=self.lower_bounds
        )
