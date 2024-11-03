from fastapi import APIRouter
from app.core.cryptoSystem import elgamal
from pydantic import BaseModel
from typing import Tuple

router = APIRouter()


class GenerateKeyResponse(BaseModel):
    privateKey: elgamal.PrivateKey
    publicKey: elgamal.PublicKey


class EncryptRequest(BaseModel):
    publicKey: elgamal.PublicKey
    message: int


class EncryptResponse(BaseModel):
    encrypted_message: Tuple[int, int]


class DecryptRequest(BaseModel):
    privateKey: elgamal.PrivateKey
    encrypted_message: Tuple[int, int]


class DecryptResponse(BaseModel):
    decrypted_message: int


@router.post("/elgamal/generate_key", response_model=GenerateKeyResponse)
async def elgamal_generate_key(seed: elgamal.Seed):
    private_key, public_key = elgamal.generateKey(seed)
    return {"privateKey": private_key, "publicKey": public_key}


@router.post("/elgamal/encrypt", response_model=EncryptResponse)
async def elgamal_encrypt(req: EncryptRequest) -> EncryptResponse:
    return EncryptResponse(
        encrypted_message=elgamal.encrypt(req.publicKey, req.message)
    )


@router.post("/elgamal/decrypt", response_model=DecryptResponse)
async def elgamal_decrypt(req: DecryptRequest) -> DecryptResponse:
    return DecryptResponse(
        decrypted_message=elgamal.decrypt(req.privateKey, req.encrypted_message)
    )
