from sqlalchemy.orm import Session

from src.modules.users.models import User
from src.modules.vehicles.models import Vehicle
from src.modules.vehicles.repository import VehicleRepository
from src.modules.vehicles.schemas import VehicleCreate, VehicleUpdate
from src.shared.errors import NotFoundError


class VehicleService:
    def __init__(self, db: Session):
        self.repository = VehicleRepository(db)

    def list_vehicles(self, skip: int = 0, limit: int = 100, status: str | None = None) -> tuple[list[Vehicle], int]:
        return self.repository.list(skip=skip, limit=limit, status=status), self.repository.count(status=status)

    def get_vehicle(self, vehicle_id: int) -> Vehicle:
        vehicle = self.repository.get_by_id(vehicle_id)
        if not vehicle:
            raise NotFoundError("Vehicle not found")
        return vehicle

    def create_vehicle(self, payload: VehicleCreate, owner: User) -> Vehicle:
        vehicle = Vehicle(**payload.model_dump(), owner_id=owner.id)
        return self.repository.create(vehicle)

    def update_vehicle(self, vehicle_id: int, payload: VehicleUpdate) -> Vehicle:
        vehicle = self.get_vehicle(vehicle_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(vehicle, field, value)
        return self.repository.update(vehicle)

    def delete_vehicle(self, vehicle_id: int) -> None:
        vehicle = self.get_vehicle(vehicle_id)
        self.repository.delete(vehicle)
