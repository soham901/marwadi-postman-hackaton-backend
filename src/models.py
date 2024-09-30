from sqlmodel import SQLModel, Field, Relationship, JSON
from typing import Optional, List
from datetime import datetime

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


class AllocationResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="medicinerequest.id", index=True)
    total_cost: float
    suppliers: List[dict] = Field(sa_column=Field(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MedicineRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hospital_id: int = Field(foreign_key="hospital.id", index=True)
    name: str
    quantity: int
    per_unit_cost: float
    distance: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    allocations: List["AllocationResult"] = Relationship(back_populates="request")


AllocationResult.request = Relationship(back_populates="allocations")


SQLModel.metadata.create_all(engine)
