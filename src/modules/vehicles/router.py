from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.users.models import User
from src.modules.vehicles.schemas import VehicleCreate, VehicleRead, VehicleUpdate
from src.modules.vehicles.service import VehicleService
from src.shared.auth import require_admin, require_roles
from src.shared.responses import ok

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.get("")
def list_vehicles(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("viewer", "admin")),
):
    vehicles, total = VehicleService(db).list_vehicles(skip=skip, limit=limit, status=status_filter)
    data = [VehicleRead.model_validate(vehicle).model_dump(mode="json") for vehicle in vehicles]
    return ok("Vehicles retrieved successfully", data, meta={"skip": skip, "limit": limit, "total": total})


@router.get("/{vehicle_id}")
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("viewer", "admin")),
):
    vehicle = VehicleService(db).get_vehicle(vehicle_id)
    return ok("Vehicle retrieved successfully", VehicleRead.model_validate(vehicle).model_dump(mode="json"))


@router.post("", status_code=status.HTTP_201_CREATED)
def create_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    vehicle = VehicleService(db).create_vehicle(payload, current_user)
    return ok("Vehicle created successfully", VehicleRead.model_validate(vehicle).model_dump(mode="json"), status=201)


@router.put("/{vehicle_id}")
def update_vehicle(
    vehicle_id: int,
    payload: VehicleUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    vehicle = VehicleService(db).update_vehicle(vehicle_id, payload)
    return ok("Vehicle updated successfully", VehicleRead.model_validate(vehicle).model_dump(mode="json"))


@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    VehicleService(db).delete_vehicle(vehicle_id)
    return ok("Vehicle deleted successfully")
