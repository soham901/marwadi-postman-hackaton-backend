from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from geopy.distance import geodesic

from app.algos.allocation import process_allocation, AllocationResponse, Input, Strategy
from app.api.v1.hospitals.models import Hospital
from app.api.v1.listings.models import Listing
from app.db.session import get_session


router = APIRouter()


class ListingWithDistance(BaseModel):
    id: int
    hospital_id: int
    name: str
    description: str
    quantity: int
    per_unit_cost: float
    distance: float
    hospital_name: str


@router.post("/allocate")
def allocate(
    session: Session = Depends(get_session),
    request_volume: int = 0,
    latitude: float = 0,
    longitude: float = 0,
    strategy: Strategy = Strategy.greedy
):
    query = select(Listing, Hospital).join(Hospital, Listing.hospital_id == Hospital.id)
    results = session.exec(query).all()

    listings_with_distance: List[ListingWithDistance] = []

    for listing, hospital in results:
        distance = geodesic((hospital.latitude, hospital.longitude), (latitude, longitude)).km
        
        listing_with_distance = ListingWithDistance(
            id=listing.id,
            hospital_id=listing.hospital_id,
            name=listing.name,
            description=listing.description,
            quantity=listing.quantity,
            per_unit_cost=listing.per_unit_cost,
            distance=round(distance, 2),
            hospital_name=hospital.name
        )
        listings_with_distance.append(listing_with_distance)

    total_cost, suppliers = process_allocation(request_volume, listings_with_distance, strategy)

    return {
        "message": "Allocation data processed",
        "total_cost": total_cost,
        "suppliers": suppliers,
    }