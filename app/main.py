from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import hospitals, listings
from app.db.session import engine
from sqlmodel import SQLModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(hospitals.router, prefix="/api/v1/hospitals", tags=["hospitals"])
app.include_router(listings.router, prefix="/api/v1/listings", tags=["listings"])
