from fastapi import status, APIRouter, Request
from fastapi.responses import RedirectResponse


router = APIRouter(
    prefix="/api/seam",
    tags=["Seam Locks"]
)

@router.post("/lock/<lock_id>", status_code=status.HTTP_200_OK)
async def lock(request: Request, lock_id: str):
    try:
        