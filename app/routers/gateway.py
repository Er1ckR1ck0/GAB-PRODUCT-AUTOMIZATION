from fastapi import status, APIRouter, Request
from fastapi.responses import JSONResponse
from ..models.event import Event
import httpx
from ..modules.lock_modules import locks

router = APIRouter(
    prefix="/api/gateway",
    tags=["Gateway"]
)

async def post_request(url: str, info: dict) -> dict:
    async with httpx.AsyncClient() as client:
        print(f"info {info}")
        response = await client.post(url, data=info)
        if response.status_code == 200:
            return {"message": "Данные отправлены"}
        else:
            return {"error": response.json()}

@router.post("/main", status_code=status.HTTP_200_OK)
async def gateway(request: Request):
    try:
        body = await request.json()
        event = Event(**body)
        event_dump = event.model_dump_json()
        print(event_dump)

        if event.data_.status == 0:
            if event.data_.cooperator_id in locks:
                return await post_request("http://localhost:8000/api/seam/lock/create_access_code", event_dump)
            else:
                return await post_request("http://localhost:8000/api/seam/mail/send_notification", event_dump)
        elif event.data_.status == 3:
            response = await post_request("http://localhost:8000/api/seam/lock", event_dump)
            if response.get("message"):
                return {"message": "Сообщение на 'Ожидание предоплаты' отправлено"}
            else:
                return {"error": "Ошибка отправки Сообщение на 'Ожидание предоплаты'"}
        else:
            return {"error": "Неизвестный статус"}
    except Exception as e:
        print(e)
        return {"error": f"Произошла ошибка: {e}"}