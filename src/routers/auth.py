from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from src.models import User
from src.schemas import UserCreate, UserRead
from src.dependencies import get_session
from src.security import get_password_hash, verify_password, create_access_token

router = APIRouter()


@router.post("/token")
def get_token(
    form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
):
    # Check if user exists in the database
    db_user = session.exec(select(User).where(User.email == form.username)).first()
    if not db_user or not verify_password(form.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Create and return an access token
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/login")
def login(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
