from pydantic.dataclasses import dataclass


@dataclass
class Location:
    longitude: float
    latitude: float

    def __init__(self, longitude: float, latitude: float):
        self.longitude = longitude
        self.latitude = latitude
