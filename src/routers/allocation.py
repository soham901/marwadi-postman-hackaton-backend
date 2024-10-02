from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from src.models import AllocationResult, MedicineRequest, User
from src.schemas import (
    AllocationResultCreate,
    AllocationResultRead,
    AllocationResult as AllocationResultSchema,
)
from src.dependencies import get_session
from src.security import get_current_user

router = APIRouter(prefix="/allocations", tags=["allocations"])


@router.post("/", response_model=AllocationResultRead)
def create_allocation(
    allocation: AllocationResultCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    db_allocation = AllocationResult(**allocation.dict())
    session.add(db_allocation)
    session.commit()
    session.refresh(db_allocation)
    return db_allocation


@router.get("/", response_model=List[AllocationResultSchema])
def read_allocations(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    allocations = session.exec(select(AllocationResult).offset(skip).limit(limit)).all()
    return allocations


@router.get("/{allocation_id}", response_model=AllocationResultSchema)
def read_allocation(
    allocation_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    allocation = session.get(AllocationResult, allocation_id)
    if allocation is None:
        raise HTTPException(status_code=404, detail="Allocation result not found")
    return allocation


@router.delete("/{allocation_id}", response_model=AllocationResultSchema)
def delete_allocation(
    allocation_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    allocation = session.get(AllocationResult, allocation_id)
    if allocation is None:
        raise HTTPException(status_code=404, detail="Allocation result not found")
    session.delete(allocation)
    session.commit()
    return allocation


@router.get("/request/{request_id}", response_model=AllocationResultSchema)
def read_allocation_by_request(
    request_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    allocation = session.exec(
        select(AllocationResult).where(AllocationResult.request_id == request_id)
    ).first()
    if allocation is None:
        raise HTTPException(
            status_code=404, detail="Allocation result not found for this request"
        )
    return allocation
