from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from src.models import Medicine
from src.schemas import (
    MedicineCreate,
    MedicineRead,
    MedicineUpdate,
    MedicineWithHospital,
)
from src.dependencies import get_session

router = APIRouter(prefix="/medicines", tags=["medicines"])


@router.post("/", response_model=MedicineRead)
def create_medicine(
    medicine: MedicineCreate,
    session: Session = Depends(get_session),
):
    db_medicine = Medicine(**medicine.dict())
    session.add(db_medicine)
    session.commit()
    session.refresh(db_medicine)
    return db_medicine


@router.get("/", response_model=List[MedicineRead])
def read_medicines(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    medicines = session.exec(select(Medicine).offset(skip).limit(limit)).all()
    return medicines


@router.get("/{medicine_id}", response_model=MedicineWithHospital)
def read_medicine(
    medicine_id: int,
    session: Session = Depends(get_session),
):
    medicine = session.get(Medicine, medicine_id)
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine


@router.put("/{medicine_id}", response_model=MedicineRead)
def update_medicine(
    medicine_id: int,
    medicine_update: MedicineUpdate,
    session: Session = Depends(get_session),
):
    db_medicine = session.get(Medicine, medicine_id)
    if db_medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")

    medicine_data = medicine_update.dict(exclude_unset=True)
    for key, value in medicine_data.items():
        setattr(db_medicine, key, value)

    session.add(db_medicine)
    session.commit()
    session.refresh(db_medicine)
    return db_medicine


@router.delete("/{medicine_id}", response_model=MedicineRead)
def delete_medicine(
    medicine_id: int,
    session: Session = Depends(get_session),
):
    medicine = session.get(Medicine, medicine_id)
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    session.delete(medicine)
    session.commit()
    return medicine
