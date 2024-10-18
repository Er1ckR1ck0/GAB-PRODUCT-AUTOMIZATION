from fastapi import status, APIRouter, Request
from fastapi.responses import JSONResponse
import httpx
from ..modules.lock import locks

router = APIRouter(
    prefix="/api/gateway",
    tags=["Gateway"]
)

async def post_request(url: str, info: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=info)
        if response.status_code == 200:
            return {"message": "Данные отправлены"}
        else:
            return {"error": response.json()}

@router.get("/", status_code=status.HTTP_200_OK)
async def gateway(request: Request):
    return {"message": "Hello, World!"}

@router.post("/main", status_code=status.HTTP_200_OK)
async def gateway(request: Request):
    try:
        body = await request.json()
        event = Event(**body)
        if event.event_ in ["event-create-record", "event-update-record"]:
            match event.data_.status:
                case 0:
                    if event.data_.cooperator_id in locks:
                        return await post_request("http://localhost:8000/api/seam/lock/create_access_code", event.model_dump_json())
                case 3:
                    response = await post_request("http://localhost:8000/api/seam/lock", event.model_dump_json())
                    if response.get("message"):
                        return {"message": "Сообщение на 'Ожидание предоплаты' отправлено"}
                    else:
                        return {"error": "Ошибка отправки Сообщение на 'Ожидание предоплаты'"}
                case _:
                    return {"error": "Неизвестный статус"}
    except Exception as e:
        print(e)
        return {"error": f"Произошла ошибка: {e}"}