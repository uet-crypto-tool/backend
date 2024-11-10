from fastapi import APIRouter
from app.core.signatureScheme import elgamal
from app.schemas.elgamal import (
    Seed,
    PrivateKey,
    PublicKey,
    GenerateKeyResponse,
    SignRequest,
    Signature,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
)

router = APIRouter()


@router.post("/elgamal/generate_key", response_model=GenerateKeyResponse)
async def elgamal_generate_key(seed: Seed):
    p, a, alpha, beta = elgamal.generateKey(int(seed.p), int(seed.a))
    return GenerateKeyResponse(
        privateKey=PrivateKey(p=str(p), a=str(a), alpha=str(alpha)),
        publicKey=PublicKey(p=str(p), alpha=str(alpha), beta=str(beta)),
    )


@router.post("/elgamal/sign", response_model=SignResponse)
async def elgamal_sign(
    req: SignRequest,
) -> SignResponse:
    y1, y2 = elgamal.sign(
        int(req.privateKey.p),
        int(req.privateKey.a),
        int(req.privateKey.alpha),
        req.message,
    )
    signature = Signature(y1=str(y1), y2=str(y2))
    return SignResponse(signature=signature)


@router.post("/elgamal/verify", response_model=VerifyResponse)
async def elgamal_verify(
    req: VerifyRequest,
) -> VerifyResponse:
    is_valid = elgamal.verify(
        int(req.publicKey.p),
        int(req.publicKey.alpha),
        int(req.publicKey.beta),
        req.message,
        (int(req.signature.y1), int(req.signature.y2)),
    )
    return VerifyResponse(is_valid=is_valid)
