from fastapi import APIRouter
from app.core.signatureScheme import elgamal
from pydantic import BaseModel
from typing import Tuple

router = APIRouter()


class GenerateKeyResponse(BaseModel):
    privateKey: elgamal.PrivateKey
    publicKey: elgamal.PublicKey


class SignRequest(BaseModel):
    privateKey: elgamal.PrivateKey
    message: int


class SignResponse(BaseModel):
    signature: Tuple[int, int]


class VerifyRequest(BaseModel):
    publicKey: elgamal.PublicKey
    message: int
    signature: Tuple[int, int]


class VerifyResponse(BaseModel):
    is_valid: bool


@router.post("/elgamal/generate_key",
             response_model=GenerateKeyResponse)
async def elgamal_generateKey(seed: elgamal.Seed):
    privateKey, publicKey = elgamal.generateKey(seed)
    return {
        "privateKey": privateKey,
        "publicKey": publicKey,
    }


@router.post("/elgamal/sign", response_model=SignResponse)
async def elgamal_sign(req: SignRequest) -> SignResponse:
    return SignResponse(
        signature=elgamal.sign(req.privateKey, req.message)
    )


@router.post("/elgamal/verify", response_model=VerifyResponse)
async def elgamal_verify(req: VerifyRequest) -> VerifyResponse:
    return VerifyResponse(
        is_valid=elgamal.verify(req.publicKey, req.message, req.signature)
    )
