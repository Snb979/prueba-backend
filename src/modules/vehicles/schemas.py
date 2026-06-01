from pydantic import BaseModel, ConfigDict, Field


class VehicleBase(BaseModel):
    brand: str = Field(min_length=2, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=2, max_length=100)
    applicant: str = Field(min_length=2, max_length=100)
    status: str = Field(min_length=2, max_length=50)


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    brand: str | None = Field(default=None, min_length=2, max_length=100)
    model: str | None = Field(default=None, min_length=1, max_length=100)
    location: str | None = Field(default=None, min_length=2, max_length=100)
    applicant: str | None = Field(default=None, min_length=2, max_length=100)
    status: str | None = Field(default=None, min_length=2, max_length=50)


class VehicleRead(VehicleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int | None = None
