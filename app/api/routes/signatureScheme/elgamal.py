from fastapi import APIRouter
from app.core.signatureScheme import elgamal
from app.schemas.elgamal import (
    GenerateKeyResponse,
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
)

router = APIRouter()


@router.post("/elgamal/generate_key", response_model=GenerateKeyResponse)
async def elgamal_generateKey(seed: elgamal.Seed):
    privateKey, publicKey = elgamal.generateKey(seed)
    return GenerateKeyResponse(
        privateKey=privateKey,
        publicKey=publicKey,
    )


@router.post("/elgamal/sign", response_model=SignResponse)
async def elgamal_sign(
    req: SignRequest,
) -> SignResponse:
    return SignResponse(signature=elgamal.sign(req.privateKey, req.message))


@router.post("/elgamal/verify", response_model=VerifyResponse)
async def elgamal_verify(
    req: VerifyRequest,
) -> VerifyResponse:
    return VerifyResponse(
        is_valid=elgamal.verify(req.publicKey, req.message, req.signature)
    )
