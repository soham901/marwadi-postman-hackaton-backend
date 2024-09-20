from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from .models import Listing

router = APIRouter()

@router.post("/", response_model=Listing)
def create_listing(listing: Listing, session: Session = Depends(get_session)):
    session.add(listing)
    session.commit()
    session.refresh(listing)
    return listing


@router.get("/{listing_id}", response_model=Listing)
def get_listing(listing_id: int, session: Session = Depends(get_session)):
    listing = session.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@router.get("/")
def get_listings(session: Session = Depends(get_session)):
    statement = select(Listing)
    results = session.exec(statement).all()
    return results
