from fastapi import APIRouter
from app.core.cryptoSystem import elgamal
from pydantic import BaseModel
from typing import Tuple

router = APIRouter()


@router.post("/elgamal/generate_key")
async def elgamal_generate_key(seed: elgamal.Seed):
    private_key, public_key = elgamal.generateKey(seed)
    return {
        "privateKey": private_key,
        "publicKey": public_key
    }


class elgamal_EncryptRequest(BaseModel):
    publicKey: elgamal.PublicKey
    message: int


@router.post("/elgamal/encrypt")
async def elgamal_encrypt(req: elgamal_EncryptRequest):
    return elgamal.encrypt(req.publicKey, req.message)


class elgamal_DecryptRequest(BaseModel):
    privateKey: elgamal.PrivateKey
    encrypted_message: Tuple[int, int]


@router.post("/elgamal/decrypt")
async def elgamal_decrypt(req: elgamal_DecryptRequest):
    return elgamal.decrypt(req.privateKey, req.encrypted_message)
