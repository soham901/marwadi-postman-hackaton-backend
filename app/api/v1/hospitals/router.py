from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from .models import Hospital

router = APIRouter()

@router.post("/", response_model=Hospital)
def create_hospital(hospital: Hospital, session: Session = Depends(get_session)):
    session.add(hospital)
    session.commit()
    session.refresh(hospital)
    return hospital

@router.get("/{hospital_id}", response_model=Hospital)
def get_hospital(hospital_id: int, session: Session = Depends(get_session)):
    hospital = session.get(Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital

@router.get("/")
def get_hospitals(session: Session = Depends(get_session)):
    statement = select(Hospital)
    results = session.exec(statement).all()
    return results

@router.delete("/{hospital_id}", status_code=204)
def delete_hospital(hospital_id: int, session: Session = Depends(get_session)):
    hospital = session.get(Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    session.delete(hospital)
    session.commit()
    return