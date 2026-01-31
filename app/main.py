from fastapi import FastAPI

from app.core.config import settings
from app.api.tasks import router as tasks_router

app = FastAPI(title=settings.app_name)

app.include_router(tasks_router)


@app.get("/ping")
async def ping():
    return {"status": "ok"}
