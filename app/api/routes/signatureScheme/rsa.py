from fastapi import APIRouter
from app.core.signatureScheme import rsa
from app.schemas.rsa import (
    GenerateKeyResponse,
    SignRequest,
    SignRespone,
    VerifyRequest,
    VerifyResponse,
)

router = APIRouter()


@router.post("/rsa/generate_key", response_model=GenerateKeyResponse)
async def rsa_generate_key(seed: rsa.Seed):
    private_key, public_key = rsa.generateKey(seed)
    return GenerateKeyResponse(privateKey=private_key, publicKey=public_key)


@router.post("/rsa/sign", response_model=SignRespone)
async def rsa_sign(req: SignRequest) -> SignRespone:
    return SignRespone(signature=rsa.sign(req.privateKey, req.message))


@router.post("/rsa/verify", response_model=VerifyResponse)
async def rsa_verify(req: VerifyRequest) -> VerifyResponse:
    return VerifyResponse(
        is_valid=rsa.verify(req.publicKey, req.message, req.signature)
    )
