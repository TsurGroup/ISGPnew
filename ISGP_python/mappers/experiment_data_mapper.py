import numpy as np
from models.experiment_data import ExperimentData
from view_models.experiment_data_view import ExperimentDataView, ImaginaryImpedanceGraph, RealImpedanceGraph
from view_models.graph_view import PointData

def get_data_set_data(data_set: ExperimentData, real_impedance_graph: list[PointData], imaginary_impedance_graph: list[PointData]):
    for i in range(len(data_set.frequency)):
        real_impedance = PointData()
        real_impedance.x = 2*np.pi*data_set.frequency[i]
        real_impedance.y = data_set.real_impedance[i]
        
        imaginary_impedance = PointData()
        imaginary_impedance.x = 2*np.pi*data_set.frequency[i]
        imaginary_impedance.y = -data_set.imaginary_impedance[i]
        
      
        real_impedance_graph.append(real_impedance)
        imaginary_impedance_graph.append(imaginary_impedance)
       

def get_experiment_data_view(data_set1: ExperimentData, data_set2: ExperimentData) -> ExperimentDataView:
    experiment_data = ExperimentDataView()
    real_impedance_graph = RealImpedanceGraph()
    imaginary_impedance_graph = ImaginaryImpedanceGraph()

    get_data_set_data(data_set1, real_impedance_graph.dataset1, imaginary_impedance_graph.dataset1)
    get_data_set_data(data_set2, real_impedance_graph.dataset2, imaginary_impedance_graph.dataset2)
    
    experiment_data.realImpedanceGraph = real_impedance_graph
    experiment_data.imaginaryImpedanceGraph = imaginary_impedance_graph

    return experiment_data