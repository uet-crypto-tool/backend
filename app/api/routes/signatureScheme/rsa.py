from fastapi import APIRouter
from app.core.signatureScheme import rsa
from pydantic import BaseModel

router = APIRouter()


@router.post("/rsa/generate_key")
async def rsa_generateKey(seed: rsa.Seed):
    private_key, public_key = rsa.generateKey(seed)
    return {
        "privateKey": private_key,
        "publicKey": public_key
    }


class RsaSignRequest(BaseModel):
    privateKey: rsa.PrivateKey
    message: int


@router.post("/rsa/sign")
async def rsa_sign(req: RsaSignRequest):
    return rsa.sign(req.privateKey, req.message)


class RsaVerifyRequest(BaseModel):
    publicKey: rsa.PublicKey
    message: int
    signature: int


@router.post("/rsa/verify")
async def rsa_verify(req: RsaVerifyRequest):
    return rsa.verify(req.publicKey, req.message, req.signature)
