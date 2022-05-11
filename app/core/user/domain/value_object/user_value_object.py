from enum import Enum


class UserType(Enum):
    RIDER = "RIDER"
    STORE_MANAGER = "STORE_MANAGER"
    SHELTER_MANAGER = "SHELTER_MANAGER"


class PersonalInfo:
    first_name: str
    last_name: str

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
