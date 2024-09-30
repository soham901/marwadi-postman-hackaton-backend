from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from src.models import MedicineRequest, User
from src.schemas import (
    RequestCreate,
    RequestRead,
    MedicineRequest as MedicineRequestSchema,
)
from src.dependencies import get_session
from src.security import get_current_user

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("/", response_model=RequestRead)
def create_request(
    request: RequestCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    db_request = MedicineRequest(**request.dict())
    session.add(db_request)
    session.commit()
    session.refresh(db_request)
    return db_request


@router.get("/", response_model=List[MedicineRequestSchema])
def read_requests(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    requests = session.exec(select(MedicineRequest).offset(skip).limit(limit)).all()
    return requests


@router.get("/{request_id}", response_model=MedicineRequestSchema)
def read_request(
    request_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    request = session.get(MedicineRequest, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


@router.delete("/{request_id}", response_model=MedicineRequestSchema)
def delete_request(
    request_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    request = session.get(MedicineRequest, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    session.delete(request)
    session.commit()
    return request
