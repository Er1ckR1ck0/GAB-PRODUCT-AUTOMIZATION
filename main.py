from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import mail, lock_router, gateway

import uvicorn

app = FastAPI(
    title="GAB-PRODUCT-AUTOMIZATION",
    version="v2.10",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(lock_router.router)
app.include_router(gateway.router)
app.include_router(mail.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)