from fastapi import APIRouter
from app.cryptoSystem.classic import Shift

router = APIRouter()


@router.get("/encode")
async def encode(msg: str):
    cipher = Shift.encode(msg)
    return cipher


@router.get("/decode")
async def decode(cipher: str):
    msg = Shift.encode(cipher)
    return msg
