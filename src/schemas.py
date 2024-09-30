from pydantic import BaseModel
from typing import List, Optional


class UserCreate(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    email: str


class HospitalCreate(BaseModel):
    name: str
    address: str


class HospitalRead(BaseModel):
    id: int
    name: str
    address: str


class MedicineCreate(BaseModel):
    name: str
    description: str
    hospital_id: int


class MedicineRead(BaseModel):
    id: int
    name: str
    description: str
    hospital_id: int


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
    per_unit_cost: float
    distance: float


class RequestRead(RequestCreate):
    id: int


class MedicineRequest(RequestRead):
    pass
