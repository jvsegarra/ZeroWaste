from typing import Optional

from pydantic import BaseModel

from app.core.store.domain.value_object.store_value_object import Location


class LocationApiDto(BaseModel):
    longitude: float
    latitude: float

    @staticmethod
    def from_location(location: Location):
        return LocationApiDto(longitude=location.longitude, latitude=location.latitude)


class StoreApiDto(BaseModel):
    name: str
    description: Optional[str] = None
    location: LocationApiDto
