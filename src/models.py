from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from src.dependencies import engine


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    hashed_password: str = Field(exclude=True)


class Hospital(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    address: str
    medicines: List["Medicine"] = Relationship(back_populates="hospital")


class Medicine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    hospital_id: Optional[int] = Field(default=None, foreign_key="hospital.id")
    hospital: Optional[Hospital] = Relationship(back_populates="medicines")


class MedicineRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hospital_id: int = Field(foreign_key="hospital.id")
    name: str
    quantity: int
    per_unit_cost: float
    distance: float


SQLModel.metadata.create_all(engine)
