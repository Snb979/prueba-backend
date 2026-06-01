from sqlalchemy.orm import Session

from src.modules.vehicles.models import Vehicle


class VehicleRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, skip: int = 0, limit: int = 100, status: str | None = None) -> list[Vehicle]:
        query = self.db.query(Vehicle)
        if status:
            query = query.filter(Vehicle.status == status)
        return query.offset(skip).limit(limit).all()

    def count(self, status: str | None = None) -> int:
        query = self.db.query(Vehicle)
        if status:
            query = query.filter(Vehicle.status == status)
        return query.count()

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def create(self, vehicle: Vehicle) -> Vehicle:
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def update(self, vehicle: Vehicle) -> Vehicle:
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        self.db.delete(vehicle)
        self.db.commit()
