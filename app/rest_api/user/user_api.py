from http import HTTPStatus

from fastapi import APIRouter, Depends
from pydantic import EmailStr
from starlette.responses import Response

from app.core.shared.value_object.common import EntityId
from app.core.user.application.signup_user import SignupUserCommand, PersonalInfoCommand
from app.core.user.domain.entity.user import User
from app.di.user import get_current_user, get_signup_user_handler, get_get_user_handler, get_delete_user_handler
from app.rest_api.user.dto import UserRequestApiDto, UserResponseApiDto

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.post("/", status_code=HTTPStatus.CREATED)
async def signup_user(user_request: UserRequestApiDto, signup_user_handler=Depends(get_signup_user_handler)):
    user_id = await signup_user_handler.handle(
        SignupUserCommand(
            email=user_request.email,
            password=user_request.password,
            personal_info=PersonalInfoCommand(
                first_name=user_request.personal_info.first_name, last_name=user_request.personal_info.last_name
            ),
            user_type=user_request.user_type,
        )
    )

    return {"user_id": user_id.to_str()}


@user_router.get("/me", response_model=UserResponseApiDto)
async def get_current_user(user: User = Depends(get_current_user)):
    return UserResponseApiDto(
        email=EmailStr(user.email),
        user_type=user.user_type,
    )


@user_router.get("/{user_id}", response_model=UserResponseApiDto)
async def get_user(user_id, get_user_handler=Depends(get_get_user_handler)):
    user = await get_user_handler.handle(EntityId.from_str(user_id))

    return UserResponseApiDto(
        email=EmailStr(user.email),
        user_type=user.user_type,
    )


@user_router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id, delete_user_handler=Depends(get_delete_user_handler)):
    await delete_user_handler.handle(EntityId.from_str(user_id))

    return Response(status_code=HTTPStatus.NO_CONTENT)
