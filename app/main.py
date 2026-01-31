from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.api.tasks import router as tasks_router
from app.web.views import router as web_router

app = FastAPI(title=settings.app_name)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(tasks_router)
app.include_router(web_router)


@app.get("/ping")
async def ping():
    return {"status": "ok"}
