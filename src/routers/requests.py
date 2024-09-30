from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.dependencies import get_session
from src.models import MedicineRequest
from src.schemas import RequestCreate

router = APIRouter()


@router.post("/requests/")
def create_request(request: RequestCreate, session: Session = Depends(get_session)):
    session.add(MedicineRequest(**request.dict()))
    session.commit()
    session.refresh(request)
    return request
