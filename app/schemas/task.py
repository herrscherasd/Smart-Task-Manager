from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    original_text: str


class TaskRead(BaseModel):
    id: int
    original_text: str
    title: Optional[str]
    priority: Optional[str]
    category: Optional[str]
    estimated_minutes: Optional[int]
    subtasks: Optional[str]

    class Config:
        from_attributes = True
