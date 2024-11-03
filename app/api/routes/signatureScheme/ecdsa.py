from fastapi import APIRouter
from app.core.signatureScheme import ecdsa
from app.schemas.ecdsa_schemas import (
    GenerateKeyResponse,
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
)

router = APIRouter()


@router.post("/ecdsa/generate_key", response_model=GenerateKeyResponse)
async def ecdsa_generateKey(seed: ecdsa.Seed):
    privateKey, publicKey = ecdsa.generateKey(seed.curve_name)
    return GenerateKeyResponse(privateKey=privateKey, publicKey=publicKey)


@router.post("/ecdsa/sign", response_model=SignResponse)
async def ecdsa_sign(req: SignRequest) -> SignResponse:
    return SignResponse(signature=ecdsa.sign(req.privateKey, req.message))


@router.post("/ecdsa/verify", response_model=VerifyResponse)
async def ecdsa_verify(req: VerifyRequest) -> VerifyResponse:
    return VerifyResponse(
        is_valid=ecdsa.verify(req.publicKey, req.message, req.signature)
    )
