from contextlib import asynccontextmanager

from sqlalchemy import text
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.dependencies import engine, Session

# from src.algo import start_allocation_algorithm
from .routers import hospital, medicine, auth, requests, allocation


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start_allocation_algorithm()
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
app.include_router(allocation.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Hospital Management API"}


@app.get("/delete-db")
async def delete_db(secret: str):
    if secret != "superman123":
        raise HTTPException(
            status_code=400,
            detail="Incorrect secret",
        )

    try:
        # Start a session
        with Session(engine) as session:
            # Get all table names
            result = session.execute(
                text("SELECT name FROM sqlite_master WHERE type='table';")
            )
            tables = result.fetchall()

            # Disable foreign key constraints to prevent issues during deletion
            session.execute(text("PRAGMA foreign_keys = OFF;"))

            # Delete all records from each table
            for table in tables:
                table_name = table[0]
                if table_name != "sqlite_sequence":  # Skip SQLite internal table
                    session.execute(text(f"DELETE FROM {table_name};"))
                    session.commit()

            # Re-enable foreign key constraints
            session.execute(text("PRAGMA foreign_keys = ON;"))

        return {"message": "All records deleted successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
