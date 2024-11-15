from fastapi import APIRouter
from app.core.cryptoSystem.symmetric import vigenere
from pydantic import BaseModel

router = APIRouter()


class EncryptRequest(BaseModel):
    key: str
    message: str


class EncryptResponse(BaseModel):
    encrypted_message: str


class DecryptRequest(BaseModel):
    key: str
    encrypted_message: str


class DecryptResponse(BaseModel):
    decrypted_message: str


@router.post("/vigenere/encrypt", response_model=EncryptResponse)
async def encrypt(req: EncryptRequest):
    return EncryptResponse(encrypted_message=vigenere.encrypt(req.key, req.message))


@router.post("/vigenere/decrypt", response_model=DecryptResponse)
async def decrypt(req: DecryptRequest):
    return DecryptRequest(decrypted_message=vigenere.decrypted(req.key, req.message))
