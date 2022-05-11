from pydantic import BaseModel, EmailStr

from app.core.user.domain.value_object.user_value_object import PersonalInfo, UserType


class PersonalInfoApiDto(BaseModel):
    first_name: str
    last_name: str

    @staticmethod
    def from_location(personal_info: PersonalInfo):
        return PersonalInfoApiDto(first_name=personal_info.first_name, last_name=personal_info.last_name)


class UserRequestApiDto(BaseModel):
    email: EmailStr
    password: str
    personal_info: PersonalInfoApiDto
    user_type: UserType


class UserResponseApiDto(BaseModel):
    email: EmailStr
    user_type: UserType
