from fastapi import APIRouter
from app.core.signatureScheme import ecdsa
from pydantic import BaseModel

router = APIRouter()


@router.post("/ecdsa/generate_key")
async def ecdsa_generateKey():
    return "ecdsa_generateKey"


class EcdsaSignRequest(BaseModel):
    pass


@router.post("/ecdsa/sign")
async def ecdsa_sign(req: EcdsaSignRequest):
    return "ecdsa_generateKey"


class EcdsaVerifyRequest(BaseModel):
    pass


@router.post("/ecdsa/verify")
async def ecdsa_verify(req: EcdsaVerifyRequest):
    return "ecdsa_generateKey"
