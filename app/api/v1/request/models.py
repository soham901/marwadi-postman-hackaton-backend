from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class Status(Enum):
    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"
    REJECTED = "rejected"


class ItemType(Enum):
    MEDICINE = "medicine"
    EQUIPMENT = "equipment"

class Urgency(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Request(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hospital_id: int = Field(foreign_key="hospital.id")
    item_id: int = Field(foreign_key="listing.id")
    quantity: int
    created_at: Optional[datetime] = Field(default=datetime.now())
    item_type: ItemType
    urgency: Urgency
    description: Optional[str] = None
    status: Status