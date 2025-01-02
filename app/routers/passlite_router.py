from fastapi import status, APIRouter, Request
from fastapi.responses import JSONResponse
from ..models.lock import SeamLock, Lock
from dotenv import load_dotenv
from ..modules.passlite_request import passlite_request
import os
import httpx
import logging
import re

load_dotenv(".env")

router = APIRouter(
    prefix="/api/passlite",
    tags=["PassLite"]
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_atributes(field: Lock):
    try:
        count_guests = int(field.event_data.data_.custom_field2)
        if count_guests > 1:
            pattern = r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$"
            access_list, unaccess_list = [], []
            for name in field.split(","):
                if re.match(pattern=pattern, string=name):
                    access_list.append(name)
                else:
                    unaccess_list.append(name)
            return access_list, unaccess_list
        elif (0 <= count_guests <= 1  and 
              len(field.event_data.data_.custom_field2) > 0):
            raise Exception("Кол-во гостей не может быть равно 0")
        else:
            pass
    except Exception as e:
        logger.error(f"Error occurred in generate_atributes: {e}")
        return None, e

async def generator_pass(lock):
    pass

@router.post("/create_access", status_code=status.HTTP_200_OK)
async def lock(request: Lock):
    try:
        request.access_list, request.unaccess_list = generate_atributes(request)
        logger.info(f"Lock created: {lock}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/api/seam/mail/send", data=lock.model_dump_json())
            
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