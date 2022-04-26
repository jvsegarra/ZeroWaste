import uvicorn
from fastapi import FastAPI

from app.rest_api.exception_handlers import entity_not_found_exception_handler, invalid_status_exception_handler
from app.rest_api.store.store_api import router as store_router
from config.database import database
from app.core.shared.exception.base_exceptions import EntityNotFoundException, InvalidStatusException

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Include modules
app.include_router(store_router)

# Exception handlers
app.add_exception_handler(EntityNotFoundException, entity_not_found_exception_handler)
app.add_exception_handler(InvalidStatusException, invalid_status_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
