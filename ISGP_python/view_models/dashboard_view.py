from pydantic import BaseModel, ImportString
from view_models.graph_view import PointData


class ImpadanceGraphView(BaseModel):
    dataset1: list[PointData] = []
    dataset2: list[PointData] = []
    model: list[PointData] = []

class ModelGraphView(BaseModel):
  model: list[PointData] = []


class ResidualGraphView(BaseModel):
    dataset1: list[PointData] = []
    dataset2: list[PointData] = []

class DiscrepancyGraph(BaseModel):
    currentModel: list[PointData] = []
    bestModels: list[PointData] = []
    allDiscrepancies: list[PointData] = []
    

class DashboardView(BaseModel):
    run:int = 0
    generation: int = 0
    fitness: float = 0
    area: float = 0
    modelString:ImportString = ''
    modelGraph: ModelGraphView = ModelGraphView()
    impadanceGraphView:ImpadanceGraphView = ImpadanceGraphView()
    residualGraph: ResidualGraphView = ResidualGraphView()
    discrepancyGraph:DiscrepancyGraph = DiscrepancyGraph()


