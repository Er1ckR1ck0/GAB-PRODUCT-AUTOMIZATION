from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import gateway_router, lock_router, mail_router

import uvicorn

app = FastAPI(
    title="GAB-PRODUCT-AUTOMIZATION",
    version="v2.10",
)

@app.get("/", tags=["Root"])
async def read_root():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(lock_router.router)
app.include_router(gateway_router.router)
app.include_router(mail_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)