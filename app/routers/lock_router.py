from fastapi import status, APIRouter, Request
from fastapi.responses import JSONResponse
from ..models.lock import SeamLock
from ..models.event import Event, EventLock
from dotenv import load_dotenv
import os
import httpx
import logging
import json
import requests

load_dotenv(".env")

router = APIRouter(
    prefix="/api/seam",
    tags=["Seam Locks"]
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/lock/create_access_code", status_code=status.HTTP_200_OK)
async def lock(request: EventLock):
    try:
        result = SeamLock(api_key=os.getenv("SEAM_API_KEY"), event=request).create_access_code()

        if not result or "error" in result:  # Проверяем, что результат не пустой и не содержит ошибку
            logger.error(f"Error creating lock: {result}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "Ошибка создания кода доступа", "error": result}
            )

        logger.info(f"Lock created: \n\n{result}")
        response = requests.post("https://gab-product-automization.vercel.app/api/seam/mail/send", data=result.model_dump_json(), timeout=60)

        if response.status_code == 200:
            return {"message": "Данные отправлены"}
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "Ошибка отправки данных", "error": response.json()}
            )

    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Произошла ошибка при обращении к внешнему сервису: {e}"}
        )
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Произошла ошибка: {e}"}
        )