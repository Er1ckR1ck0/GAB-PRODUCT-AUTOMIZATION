from fastapi import status, APIRouter, Request
from fastapi.responses import RedirectResponse, Response
from ..models.event import Event
import httpx


router = APIRouter(
    prefix="/api/gateway",
    tags=["Gateway"]
)
import json
@router.post("/main", status_code=status.HTTP_200_OK)
async def gateway(request: Event):
    event = request.model_dump_json()
    try:
        async with httpx.AsyncClient() as client:
            match request.DATA.status:
                case 0:  # Записано
                    response = await client.post("http://localhost:8000/api/seam/lock/create_access_code", json=request.model_dump_json())
                    if response.status_code == 200:
                        return {"message": "Данные отправлены"}
                    else:
                        print(response.json())
                        return {"error": "Ошибка отправки данных"}
                case 3:  # Ждёт Предоплаты
                    response = await client.post("http://localhost:8000/api/seam/lock", json=event)
                    if response.status_code == 200:
                        return {"message": "Сообщение на 'Ожидание предоплаты' отправлено"}
                    else:
                        return {"error": "Ошибка отправки Сообщение на 'Ожидание предоплаты'"}
                case _:
                    return {"error": "Неизвестный статус"}
    except Exception as e:
        print(e)
        return {"error": f"Произошла ошибка: {e}"}