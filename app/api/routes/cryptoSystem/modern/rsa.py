from fastapi import APIRouter
from app.cryptoSystem.modern import RSA

router = APIRouter()


@router.get("/encode")
async def encode(msg: str):
    cipher = RSA.encode(msg)
    return cipher


@router.get("/decode")
async def decode(cipher: str):
    msg = RSA.encode(cipher)
    return msg
