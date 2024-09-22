from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import StrEnum, auto

class ItemType(StrEnum):
    MEDICINE = auto()
    EQUIPMENT = auto()

class Urgency(StrEnum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

class Request(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hospital_id: int = Field(foreign_key="hospital.id")
    item_id: int = Field(foreign_key="listing.id")
    quantity: int
    created_at: Optional[datetime] = Field(default=datetime.now())
    item_type: ItemType
    urgency: Urgency