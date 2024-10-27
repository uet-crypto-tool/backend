from fastapi import APIRouter
from app.core.signatureScheme import ecdsa
from pydantic import BaseModel
from typing import Tuple

router = APIRouter()


class EcdsaSignRequest(BaseModel):
    privateKey: ecdsa.PrivateKey
    message: int


class EcdsaVerifyRequest(BaseModel):
    publicKey: ecdsa.PublicKey
    message: int
    signature: Tuple[int, int]


@router.post("/ecdsa/generate_key")
async def ecdsa_generateKey(seed: ecdsa.Seed):
    privateKey, publicKey = ecdsa.generateKey(seed.curve_domain_name)
    return {
        "privateKey": privateKey,
        "publicKey": publicKey,
    }


@router.post("/ecdsa/sign")
async def ecdsa_sign(req: EcdsaSignRequest):
    return ecdsa.sign(req.privateKey, req.message)


@router.post("/ecdsa/verify")
async def ecdsa_verify(req: EcdsaVerifyRequest):
    return ecdsa.verify(req.publicKey, req.message, req.signature)
