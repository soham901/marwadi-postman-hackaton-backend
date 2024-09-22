from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from .modles import Request

router = APIRouter()

@router.post("/", response_model=Request)
def create_request(request: Request, session: Session = Depends(get_session)):
    session.add(request)
    session.commit()
    session.refresh(request)
    return request


@router.get("/{request_id}", response_model=Request)
def get_request(request_id: int, session: Session = Depends(get_session)):
    request = session.get(Request, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="request not found")
    return request


@router.get("/")
def get_requests(session: Session = Depends(get_session)):
    statement = select(Request)
    results = session.exec(statement).all()
    return results

@router.delete("/{request_id}", status_code=204)
def delete_hospital(request_id: int, session: Session = Depends(get_session)):
    request = session.get(Request, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="request not found")
    
    session.delete(request)
    session.commit()
    return