from fastapi import APIRouter
from app.core.cryptoSystem.symmetric import affine
from pydantic import BaseModel

router = APIRouter()


class Key(BaseModel):
    a: int
    b: int


class EncryptRequest(BaseModel):
    key: Key
    message: str


class EncryptResponse(BaseModel):
    encrypted_message: str


class DecryptRequest(BaseModel):
    key: Key
    encrypted_message: str


class DecryptResponse(BaseModel):
    decrypted_message: str


@router.post(
    "/affine/encrypt",
    response_model=EncryptResponse,
    summary="Encrypt a message using the Affine cipher",
)
async def encrypt(req: EncryptRequest):
    return EncryptResponse(
        encrypted_message=affine.encrypt(req.key.a, req.key.b, req.message)
    )


@router.post(
    "/affine/decrypt",
    response_model=DecryptResponse,
    summary="Decrypt a message using the Affine cipher",
)
async def decrypt(req: DecryptRequest):
    return DecryptResponse(
        decrypted_message=affine.decrypted(req.key.a, req.key.b, req.message)
    )
