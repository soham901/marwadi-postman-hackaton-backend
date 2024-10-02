from datetime import datetime
from sqlmodel import Session, select
from src.dependencies import engine
from src.models import MedicineRequest, AllocationResult, Hospital, Medicine
from src.algo import process_allocation, Input, Strategy
from geopy.distance import geodesic


def run_allocation_task():
    with Session(engine) as session:
        requests = session.exec(select(MedicineRequest)).all()

        for request in requests:
            if not request.id:
                continue

            requesting_hospital = session.get(Hospital, request.hospital_id)
            if not requesting_hospital:
                continue

            # Get all hospitals except the requesting hospital
            all_hospitals = session.exec(
                select(Hospital).where(Hospital.id != request.hospital_id)
            ).all()

            inputs = []
            for hospital in all_hospitals:
                medicine = session.exec(
                    select(Medicine)
                    .where(Medicine.hospital_id == hospital.id)
                    .where(Medicine.name == request.name)
                ).first()

                if medicine and hospital.id:
                    distance = geodesic(
                        (requesting_hospital.latitude, requesting_hospital.longitude),
                        (hospital.latitude, hospital.longitude),
                    ).kilometers

                    inputs.append(
                        Input(
                            hospital_id=hospital.id,
                            name=request.name,
                            quantity=medicine.quantity,
                            per_unit_cost=medicine.price_per_unit,
                            distance=distance,
                        )
                    )

            if inputs:
                # Use the strategy specified in the request
                strategy = Strategy(request.strategy)
                total_cost, suppliers = process_allocation(
                    request_volume=request.quantity,
                    hospitals=inputs,
                    strategy=strategy,
                )

                allocation_result = AllocationResult(
                    request_id=request.id,
                    total_cost=total_cost,
                    suppliers=suppliers,
                )
                session.add(allocation_result)
                session.commit()

        session.close()

    return {"status": "success", "time": str(datetime.utcnow())}
