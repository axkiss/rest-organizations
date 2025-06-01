from pydantic import BaseModel


class BuildingOutSchema(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float


class PhoneOutSchema(BaseModel):
    id: int
    number: str


class ActivityOutSchema(BaseModel):
    id: int
    name: str


class OrganizationOutSchema(BaseModel):
    id: int
    name: str
    building: BuildingOutSchema
    phones: list[PhoneOutSchema]
    activities: list[ActivityOutSchema]


class OrganizationFilterSchema(BaseModel):
    building_id: int | None = None
    activity_id: int | None = None
    # include_sub_activities: bool = False
    name: str | None = None
    lat: float | None = None
    lon: float | None = None
    radius_m    : float | None = None
    lat_min: float | None = None
    lat_max: float | None = None
    lon_min: float | None = None
    lon_max: float | None = None
