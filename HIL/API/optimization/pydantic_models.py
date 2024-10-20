from pydantic import BaseModel, Field
from typing import List


class OptimizeSessionInput(BaseModel):
    session_id: str
    current_parameter: List[float]
    cost: float

class OptimizeInput(BaseModel):
    parameters: List[float]
    costs: List[float]