from sqlmodel import SQLModel, Field
from typing import Optional

class Hospital(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str]
    latitude: float
    longitude: float
