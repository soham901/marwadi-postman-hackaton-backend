from pydantic import BaseModel
from enum import Enum
from typing import List, Tuple, Dict


class Input(BaseModel):
    hospital_id: int
    name: str
    quantity: int
    per_unit_cost: float
    distance: float


class SupplierOutput(BaseModel):
    hospital: str
    volume_allocated: int


class AllocationResponse(BaseModel):
    total_cost: float
    suppliers: List[SupplierOutput]


class Strategy(str, Enum):
    greedy = "greedy"
    distance = "distance"
    cost = "cost"


def process_allocation(
    request_volume: int, hospitals: List[Input], strategy: Strategy
) -> Tuple[float, List[Dict]]:
    if request_volume < 0:
        request_volume = 0

    suppliers = []

    if strategy == Strategy.distance:
        hospitals = sorted(hospitals, key=lambda x: x.distance)
    elif strategy == Strategy.greedy:
        hospitals = sorted(
            hospitals, key=lambda x: x.distance / x.quantity, reverse=True
        )
    elif strategy == Strategy.cost:
        hospitals = sorted(hospitals, key=lambda x: x.per_unit_cost)
    else:
        raise ValueError("Invalid strategy")

    total_cost = 0.0

    for item in hospitals:
        if request_volume <= 0:
            break

        take_volume = min(request_volume, item.quantity)
        total_cost += item.per_unit_cost * take_volume
        request_volume -= take_volume

        suppliers.append(
            {
                "hospital_id": item.hospital_id,
                "name": item.name,
                "per_unit_cost": item.per_unit_cost,
                "distance": item.distance,
                "quantity": item.quantity - take_volume,
                "volume_allocated": take_volume,
            }
        )

    return total_cost, suppliers
