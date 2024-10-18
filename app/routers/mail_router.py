from fastapi import status, APIRouter
from fastapi.responses import JSONResponse
from ..models.lock import Lock
from ..models.mail import Mail
from ..models.event import EventLock
from dotenv import load_dotenv
import logging

load_dotenv()

router = APIRouter(
    prefix="/api/seam/mail",
    tags=["Mail"]
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/send", status_code=status.HTTP_200_OK)
async def send_mail(request: Lock):
    try:
        Mail(lock=request).send_message()
        return {"message": "Сообщение отправлено"}
    except Exception as e:
        logger.error(f"Error sending mail: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Произошла ошибка: {e}"}
        )

@router.post("/send_notification", status_code=status.HTTP_200_OK)
async def send_notification(request: EventLock):
    try:
        Mail(lock=request).send_message()
        return {"message": "Уведомление отправлено"}
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Произошла ошибка: {e}"}
        )