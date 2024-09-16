from fastapi import status, APIRouter, Request
from fastapi.responses import RedirectResponse
from ..models.lock import SeamLock
from ..models.event import Event
from dotenv import load_dotenv
import os
import httpx

load_dotenv(".env")

router = APIRouter(
    prefix="/api/seam",
    tags=["Seam Locks"]
)

@router.post("/lock/create_access_code", status_code=status.HTTP_200_OK)
async def lock(request: Event):
    try:
        result = SeamLock(api_key=os.getenv("SEAM_API_KEY"), event=request)
        lock = result.create_access_code()
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/api/seam/mail/send", json=lock.model_dump_json())
            if response.status_code == 200:
                return {"message": "Данные отправлены"}
            else:
                return {"error": "Ошибка отправки данных"}
    except Exception as e:
        return {"error": f"Произошла ошибка: {e}"}
    