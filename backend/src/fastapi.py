from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

# Load environment variables before other imports
load_dotenv()

from .api.config import router as config_router
from .scheduler import init_scheduler, scheduler
from .services.confluence_service import run_weekly_report_job
from .services.oncall_service import run_oncall_notification_job


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 應用程式的生命週期管理器。
    在應用程式啟動時初始化排程器，並在應用程式關閉時停止排程器。
    """
    # 應用程式啟動邏輯
    init_scheduler()
    yield
    # 應用程式關閉邏輯
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler shut down.")


class ValidationErrorHandlingRoute(APIRoute):
    """
    自定義路由類別，用於全局處理 ValueError 異常，並返回統一的 JSON 錯誤響應。
    """
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


# 初始化 FastAPI 應用程式實例，並使用自定義的錯誤處理路由和生命週期管理器。
app = FastAPI(route_class=ValidationErrorHandlingRoute, lifespan=lifespan)

# 從其他檔案中包含 API 路由
# 這是用於配置相關操作的 API 路由，例如獲取或更新應用程式配置。
app.include_router(config_router)


# --- Root and Health Check Endpoints ---
@app.get("/")
async def read_root():
    """
    根路徑的歡迎訊息，用於基本健康檢查或確認服務運行。
    """
    return {"message": "Hello, Development Team Automation Tool Backend!"}


# --- Scheduled Job Trigger Endpoints ---
@app.post("/schedule/confluence-weekly-report")
async def trigger_confluence_weekly_report():
    """
    透過 HTTP 請求觸發 Confluence 週報生成作業。
    直接呼叫 Confluence 服務層的核心邏輯。
    """
    try:
        return run_weekly_report_job()
    except Exception as e:
        # 記錄異常以便於調試
        print(f"HTTP trigger for Confluence job failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/schedule/on-call-notification")
async def trigger_on_call_notification():
    """
    透過 HTTP 請求觸發 On-call 通知作業。
    直接呼叫 On-call 服務層的核心邏輯。
    """
    try:
        return run_oncall_notification_job()
    except Exception as e:
        # 記錄異常以便於調試
        print(f"HTTP trigger for On-call job failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
