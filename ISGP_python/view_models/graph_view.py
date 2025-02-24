from pydantic import BaseModel


class PointData(BaseModel):
    x: float = 0
    y: float = 0