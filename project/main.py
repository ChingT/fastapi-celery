import logging

from celery import Celery
from celery.result import AsyncResult
from celery.signals import after_setup_logger
from config import settings
from fastapi import Body, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from worker import create_task, generate_transaction_report, send_notification

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


celery = Celery(
    __name__, broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)


logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@after_setup_logger.connect
def setup_celery_logger(logger, *args, **kwargs):
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger("tasks")
    fh = logging.FileHandler("logs/tasks.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)


@app.get("/home")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return JSONResponse(result)


@app.get("/push/{device_token}")
async def notify(device_token: str):
    logger.info("sending notification in background")
    send_notification.delay(device_token)
    return JSONResponse({"message": "Notification sent"})


@app.get("/export/report")
async def export():
    generate_transaction_report.delay()
    return JSONResponse({"message": "Generating report"})
