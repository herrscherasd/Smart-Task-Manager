from pydantic import BaseModel
from typing import Literal, List


class AIAnalysis(BaseModel):
    title: str
    priority: Literal["High", "Medium", "Low"]
    category: str
    estimated_minutes: int
    subtasks: List[str]
