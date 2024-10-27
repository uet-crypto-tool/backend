from fastapi import APIRouter
from app.core.signatureScheme import ecdsa
from pydantic import BaseModel
from typing import Tuple

router = APIRouter()


class GenerateKeyResponse(BaseModel):
    privateKey: ecdsa.PrivateKey
    publicKey: ecdsa.PublicKey


class SignRequest(BaseModel):
    privateKey: ecdsa.PrivateKey
    message: int


class SignResponse(BaseModel):
    signature: Tuple[int, int]


class VerifyRequest(BaseModel):
    publicKey: ecdsa.PublicKey
    message: int
    signature: Tuple[int, int]


class VerifyResponse(BaseModel):
    is_valid: bool


@router.post("/ecdsa/generate_key",
             response_model=GenerateKeyResponse)
async def ecdsa_generateKey(seed: ecdsa.Seed):
    privateKey, publicKey = ecdsa.generateKey(seed.curve_domain_name)
    return {
        "privateKey": privateKey,
        "publicKey": publicKey,
    }


@router.post("/ecdsa/sign", response_model=SignResponse)
async def ecdsa_sign(req: SignRequest):
    return SignResponse(
        signature=ecdsa.sign(req.privateKey, req.message)
    )


@router.post("/ecdsa/verify", response_model=VerifyResponse)
async def ecdsa_verify(req: VerifyRequest):
    return VerifyResponse(
        is_valid=ecdsa.verify(req.publicKey, req.message, req.signature)
    )
