from fastapi import APIRouter
from app.core.signatureScheme import elgamal
from pydantic import BaseModel
from typing import Tuple

router = APIRouter()


@router.post("/elgamal/generate_key")
async def elgamal_generateKey(seed: elgamal.Seed):
    privateKey, publicKey = elgamal.generateKey(seed)
    return {
        "privateKey": privateKey,
        "publicKey": publicKey,
    }


class ElgamalSignRequest(BaseModel):
    privateKey: elgamal.PrivateKey
    message: int


@router.post("/elgamal/sign")
async def elgamal_sign(req: ElgamalSignRequest):
    return elgamal.sign(req.privateKey, req.message)


class ElgamalVerifyRequest(BaseModel):
    publicKey: elgamal.PublicKey
    message: int
    signature: Tuple[int, int]


@router.post("/elgamal/verify")
async def elgamal_verify(req: ElgamalVerifyRequest):
    return elgamal.verify(req.publicKey, req.message, req.signature)
