from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from src.models import Hospital, Medicine
from src.schemas import (
    HospitalCreate,
    HospitalRead,
    HospitalWithMedicines,
    MedicineWithHospital,
)
from src.dependencies import get_session

router = APIRouter(tags=["hospitals"])


@router.post(
    "/hospitals/", response_model=HospitalRead, status_code=status.HTTP_201_CREATED
)
def create_hospital(hospital: HospitalCreate, session: Session = Depends(get_session)):
    db_hospital = Hospital(**hospital.dict())
    session.add(db_hospital)
    session.commit()
    session.refresh(db_hospital)
    return db_hospital


@router.get("/hospitals/", response_model=List[HospitalRead])
def read_hospitals(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    hospitals = session.exec(select(Hospital).offset(skip).limit(limit)).all()
    return hospitals


@router.get("/hospitals/{hospital_id}", response_model=HospitalWithMedicines)
def read_hospital(hospital_id: int, session: Session = Depends(get_session)):
    hospital = session.get(Hospital, hospital_id)
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital


# @router.get("/medicines/{medicine_id}", response_model=MedicineWithHospital)
# def read_medicine(medicine_id: int, session: Session = Depends(get_session)):
#     medicine = session.get(Medicine, medicine_id)
#     if medicine is None:
#         raise HTTPException(status_code=404, detail="Medicine not found")
#     return medicine
