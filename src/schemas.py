from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Dict, List, Optional


class Strategy(str, Enum):
    greedy = "greedy"
    distance = "distance"
    cost = "cost"


class UserCreate(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    email: str


class HospitalCreate(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float


class HospitalRead(BaseModel):
    id: int
    name: str
    address: str
    latitude: float
    longitude: float


class MedicineCreate(BaseModel):
    name: str
    description: str
    quantity: int
    price_per_unit: float
    hospital_id: int


class MedicineRead(MedicineCreate):
    id: int


class HospitalWithMedicines(HospitalRead):
    medicines: List[MedicineRead]


class MedicineWithHospital(MedicineRead):
    hospital: HospitalRead


class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    hospital_id: Optional[int] = None


class RequestCreate(BaseModel):
    hospital_id: int
    name: str
    quantity: int
    strategy: Optional[Strategy]


class RequestRead(RequestCreate):
    id: int


class MedicineRequest(RequestRead):
    pass


class AllocationResultCreate(BaseModel):
    request_id: int
    total_cost: float
    suppliers: List[Dict]


class AllocationResultRead(AllocationResultCreate):
    id: int
    created_at: datetime


class AllocationResult(AllocationResultRead):
    pass
