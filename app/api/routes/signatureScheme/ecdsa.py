from fastapi import APIRouter
from app.core.signatureScheme import ecdsa
from app.core.ellipticCurve.domain import CurveDomainParamter
from app.core.ellipticCurve.point import Point
from app.schemas.ecdsa import (
    Seed,
    GenerateKeyResponse,
    PrivateKey,
    PublicKey,
    SignRequest,
    Signature,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
)

router = APIRouter()


@router.post("/ecdsa/generate_key", response_model=GenerateKeyResponse)
async def ecdsa_generateKey(seed: Seed):
    curve_name, d, Q = ecdsa.generateKey(seed.curve_name)
    return GenerateKeyResponse(
        privateKey=PrivateKey(curve_name=curve_name, d=str(d)),
        publicKey=PublicKey(curve_name=curve_name, Q=Q.type()),
    )


@router.post("/ecdsa/sign", response_model=SignResponse)
async def ecdsa_sign(req: SignRequest) -> SignResponse:
    r, s = ecdsa.sign(
        req.privateKey.curve_name, int(req.privateKey.d), req.message
    )
    return SignResponse(signature=Signature(r=str(r), s=str(s)))


@router.post("/ecdsa/verify", response_model=VerifyResponse)
async def ecdsa_verify(req: VerifyRequest) -> VerifyResponse:
    curve = CurveDomainParamter.get(req.publicKey.curve_name)
    is_valid = ecdsa.verify(
        req.publicKey.curve_name,
        Point(curve, req.publicKey.Q.x, req.publicKey.Q.y),
        req.message,
        (int(req.signature.r), int(req.signature.s)),
    )
    return VerifyResponse(is_valid=is_valid)
