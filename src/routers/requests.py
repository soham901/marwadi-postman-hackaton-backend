from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.dependencies import get_session
from src.models import MedicineRequest
from src.schemas import RequestCreate

router = APIRouter(tags=["requests"])


@router.post("/requests/")
def create_request(data: RequestCreate, session: Session = Depends(get_session)):
    request = MedicineRequest(**data.dict())
    session.add(request)
    session.commit()
    session.refresh(request)
    return request
