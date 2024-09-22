from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.api.v1.listings.models import Listing

class Hospital(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    latitude: float
    longitude: float

    # New descriptive fields
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None

    listings: list[Listing] = Relationship(cascade_delete=True)
