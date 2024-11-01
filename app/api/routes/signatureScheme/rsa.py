from fastapi import APIRouter
from app.core.signatureScheme import rsa
from pydantic import BaseModel

router = APIRouter()


class GenerateKeyResponse(BaseModel):
    privateKey: rsa.PrivateKey
    publicKey: rsa.PublicKey


class SignRequest(BaseModel):
    privateKey: rsa.PrivateKey
    message: int


class SignRespone(BaseModel):
    signature: int


class VerifyRequest(BaseModel):
    publicKey: rsa.PublicKey
    message: int
    signature: int


class VerifyResponse(BaseModel):
    is_valid: bool


@router.post("/rsa/generate_key",
             response_model=GenerateKeyResponse)
async def rsa_generate_key(seed: rsa.Seed):
    private_key, public_key = rsa.generateKey(seed)
    return {
        "privateKey": private_key,
        "publicKey": public_key
    }


@router.post("/rsa/sign", response_model=SignRespone)
async def rsa_sign(req: SignRequest) -> SignRespone:
    return SignRespone(signature=rsa.sign(req.privateKey, req.message))


@router.post("/rsa/verify", response_model=VerifyResponse)
async def rsa_verify(req: VerifyRequest) -> VerifyResponse:
    return VerifyResponse(
        is_valid=rsa.verify(req.publicKey, req.message, req.signature)
    )
