from pydantic import BaseModel
from view_models.graph_view import PointData


class RealImpedanceGraph(BaseModel):
    dataset1: list[PointData] = []
    dataset2: list[PointData] = []

class ImaginaryImpedanceGraph(BaseModel):
    dataset1: list[PointData] = []
    dataset2: list[PointData] = []


class ExperimentDataView(BaseModel):
    realImpedanceGraph: RealImpedanceGraph = RealImpedanceGraph()
    imaginaryImpedanceGraph: ImaginaryImpedanceGraph = ImaginaryImpedanceGraph() 



    