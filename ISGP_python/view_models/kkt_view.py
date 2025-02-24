from pydantic import BaseModel
from view_models.graph_view import PointData

class RealToImaginaryGraph(BaseModel):
    kkTransform: list[PointData] = []
    realImpedance: list[PointData] = []

class ImaginaryToRealGraph(BaseModel):
    kkTransform: list[PointData] = []
    imaginaryImpedance: list[PointData] = []

class ColeColeGraph(BaseModel):
    kkTransform: list[PointData] = []
    coleCole: list[PointData] = []

class KKTGraph(BaseModel):
    realToImaginaryGraph: RealToImaginaryGraph = RealToImaginaryGraph()
    imaginaryToRealGraph: ImaginaryToRealGraph = ImaginaryToRealGraph()
    coleColeGraph: ColeColeGraph = ColeColeGraph()