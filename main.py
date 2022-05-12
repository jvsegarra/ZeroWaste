import uvicorn
from fastapi import FastAPI, APIRouter

from app.core.shared.exception.base_exceptions import EntityNotFoundException, InvalidStatusException
from app.rest_api.auth.auth_api import auth_router
from app.rest_api.exception_handlers import entity_not_found_exception_handler, invalid_status_exception_handler
from app.rest_api.store.store_api import store_router
from app.rest_api.user.user_api import user_router
from config.database import database


API_PREFIX = "/api"
API_VERSION = "v1"

app = FastAPI(title="Zero Waste")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Include api modules
api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(store_router)
api_router.include_router(user_router)

app.include_router(api_router, prefix=f"{API_PREFIX}/{API_VERSION}")

# Exception handlers
app.add_exception_handler(EntityNotFoundException, entity_not_found_exception_handler)
app.add_exception_handler(InvalidStatusException, invalid_status_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
