from dotenv import load_dotenv  # 修正：導入 load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

load_dotenv() # 修正：在應用程式啟動時加載 .env 檔案

from .api.config import router as config_router  # Import the config router
from .api.schedule import (
    router as schedule_router,  # Import the schedule router
)


class ValidationErrorHandlingRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> JSONResponse:
            try:
                return await original_route_handler(request)
            except ValueError as exc:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": str(exc)},
                )
        return custom_route_handler

app = FastAPI(route_class=ValidationErrorHandlingRoute)

# Include API routes
app.include_router(schedule_router)
app.include_router(config_router)

@app.get("/")
async def read_root():
    return {"message": "Hello, Development Team Automation Tool Backend!"}
