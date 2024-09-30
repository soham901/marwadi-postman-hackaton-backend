from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.algo import start_allocation_algorithm
from .routers import hospital, medicine, auth, requests


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_allocation_algorithm()
    yield


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(hospital.router)
app.include_router(medicine.router)
app.include_router(requests.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Hospital Management API"}
