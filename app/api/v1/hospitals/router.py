from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from .models import Hospital

router = APIRouter()

@router.post("/hospitals/", response_model=Hospital)
def create_hospital(hospital: Hospital, session: Session = Depends(get_session)):
    session.add(hospital)
    session.commit()
    session.refresh(hospital)
    return hospital

@router.get("/hospitals/{hospital_id}", response_model=Hospital)
def get_hospital(hospital_id: int, session: Session = Depends(get_session)):
    hospital = session.get(Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital


@router.get("/hospitals/")
def get_hospitals(session: Session = Depends(get_session)):
    statement = select(Hospital)
    results = session.exec(statement).all()
    return results
