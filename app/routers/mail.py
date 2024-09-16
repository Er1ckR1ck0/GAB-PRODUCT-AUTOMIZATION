from fastapi import status, APIRouter, Request
from fastapi.responses import RedirectResponse
from ..models.lock import SeamLock, Lock
from ..models.mail import Mail
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

router = APIRouter(
    prefix="/api/seam/mail",
    tags=["Mail"]
)

@router.post("/send", status_code=status.HTTP_200_OK)
async def lock(request: Lock):
    lock = await request.model_dump_json()
    try:
        mail = Mail(**lock)
        mail.send_message()
    except Exception as e:
        return {"error": f"Произошла ошибка: {e}"}
    