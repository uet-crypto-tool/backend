from fastapi import APIRouter
from app.core.signatureScheme import rsa
from app.schemas.rsa import (
    Seed,
    GenerateKeyResponse,
    SignRequest,
    SignRespone,
    VerifyRequest,
    VerifyResponse,
    Signature,
    PrivateKey,
    PublicKey,
)

router = APIRouter()


@router.post("/rsa/generate_key", response_model=GenerateKeyResponse)
async def rsa_generate_key(seed: Seed):
    n, d, e = rsa.generateKey(int(seed.p), int(seed.q))
    privateKey = PrivateKey(n=str(n), d=str(d))
    publicKey = PublicKey(n=str(n), e=str(e))
    return GenerateKeyResponse(privateKey=privateKey, publicKey=publicKey)


@router.post("/rsa/sign", response_model=SignRespone)
async def rsa_sign(req: SignRequest) -> SignRespone:
    signature = Signature(
        value=str(
            rsa.sign(int(req.privateKey.n), int(req.privateKey.d), req.message)
        )
    )
    return SignRespone(signature=signature)


@router.post("/rsa/verify", response_model=VerifyResponse)
async def rsa_verify(req: VerifyRequest) -> VerifyResponse:
    is_valid = rsa.verify(
        int(req.publicKey.n),
        int(req.publicKey.e),
        req.message,
        int(req.signature.value),
    )
    return VerifyResponse(is_valid=is_valid)
