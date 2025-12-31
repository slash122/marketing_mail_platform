from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": f"App is running, time: {datetime.timestamp(datetime.now())}"}

@router.get("/ping")
async def ping():
    return {"message": "pong"}