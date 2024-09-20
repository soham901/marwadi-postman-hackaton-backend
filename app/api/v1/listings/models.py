from sqlmodel import SQLModel, Field
from typing import Optional


class Listing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hospital_id: int = Field(foreign_key="hospital.id")
    name: str
    description: Optional[str]
    quantity: int
    per_unit_cost: float
