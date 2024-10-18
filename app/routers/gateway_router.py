from fastapi import status, APIRouter, Request
from fastapi.responses import JSONResponse
from ..models.event import Event
import httpx
from ..modules.lock import locks
import logging
logger = logging.getLogger("gateway")
logger.setLevel(logging.INFO)
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
        logger.info(f"Received event: {event}")

        if event.event_ in ["event-create-record", "event-update-record"]:
            match event.data_.status:
                case 0:
                    if event.data_.cooperator_id in locks:
                        logger.info(f"Creating access code for cooperator: {event.data_.cooperator_id}")
                        return await post_request("https://gab-product-automization.vercel.app/api/seam/lock/create_access_code", event.model_dump_json())
                case 3:
                    response = await post_request("https://gab-product-automization.vercel.app/api/seam/lock", event.model_dump_json())
                    if response.get("message"):
                        logger.info("Message sent to 'Ожидание предоплаты'")
                        return {"message": "Сообщение на 'Ожидание предоплаты' отправлено"}
                    else:
                        logger.error("Failed to send message to 'Ожидание предоплаты'")
                        return {"error": "Ошибка отправки Сообщение на 'Ожидание предоплаты'"}
                case _:
                    logger.error("Unknown status")
                    return {"error": "Неизвестный статус"}
    except Exception as e:
        logger.exception("An error occurred")
        return {"error": f"Произошла ошибка: {e}"}