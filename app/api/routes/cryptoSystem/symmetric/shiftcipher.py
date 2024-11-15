from fastapi import APIRouter
from app.core.cryptoSystem.symmetric import shiftcipher
from pydantic import BaseModel

router = APIRouter()


class EncryptRequest(BaseModel):
    key: int
    message: str


class EncryptResponse(BaseModel):
    encrypted_message: str


class DecryptRequest(BaseModel):
    key: int
    encrypted_message: str


class DecryptResponse(BaseModel):
    decrypted_message: str


@router.post("/shiftcipher/encrypt", response_model=EncryptResponse)
async def encrypt(req: EncryptRequest):
    return EncryptResponse(encrypted_message=shiftcipher.encrypt(req.key, req.message))


@router.post("/shiftcipher/decrypt", response_model=DecryptResponse)
async def decrypt(req: DecryptRequest):
    return DecryptRequest(decrypted_message=shiftcipher.decrypted(req.key, req.message))
