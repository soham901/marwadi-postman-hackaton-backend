from celery import shared_task, Celery
from celery.schedules import crontab

from datetime import datetime
from sqlmodel import Session, select
from src.dependencies import engine
from src.models import MedicineRequest, AllocationResult
from src.algo import process_allocation, Input, Strategy

celery_app = Celery(
    "allocation_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@shared_task
def run_allocation_task():
    with Session(engine) as session:
        requests = session.exec(select(MedicineRequest)).all()

        for request in requests:
            total_cost, suppliers = process_allocation(
                request_volume=request.quantity,
                hospitals=[
                    Input(
                        hospital_id=request.hospital_id,
                        name=request.name,
                        quantity=request.quantity,
                        per_unit_cost=request.per_unit_cost,
                        distance=request.distance,
                    )
                ],
                strategy=Strategy.cost,
            )

            if not request.id:
                break

            allocation_result = AllocationResult(
                request_id=request.id,
                total_cost=total_cost,
                suppliers=suppliers,
            )
            session.add(allocation_result)
            session.commit()

        session.close()

        return {"status": "success", "time": str(datetime.utcnow())}


celery_app.conf.beat_schedule = {
    "run-allocation-every-hour": {
        "task": "allocation_tasks.run_allocation_task",
        "schedule": crontab(minute=0, hour="*"),
    },
}
