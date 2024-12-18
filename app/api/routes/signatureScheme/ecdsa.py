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


@router.post(
    "/ecdsa/generate_key",
    response_model=GenerateKeyResponse,
    summary="Generates ECDSA key pairs (private and public keys) using the provided curve name.",
)
async def ecdsa_generateKey(seed: Seed):
    curve_name, d, Q = ecdsa.generateKey(seed.curve_name)
    return GenerateKeyResponse(
        privateKey=PrivateKey(curve_name=curve_name, d=str(d)),
        publicKey=PublicKey(curve_name=curve_name, Q=Q.type()),
    )


@router.post(
    "/ecdsa/sign",
    response_model=SignResponse,
    summary="Signs a message using the provided private key.",
)
async def ecdsa_sign(req: SignRequest) -> SignResponse:
    r, s = ecdsa.sign(req.privateKey.curve_name, int(req.privateKey.d), req.message)
    return SignResponse(signature=Signature(r=str(r), s=str(s)))


@router.post(
    "/ecdsa/verify",
    response_model=VerifyResponse,
    summary="Verifies if a given signature is valid for a message using the provided public key.",
)
async def ecdsa_verify(req: VerifyRequest) -> VerifyResponse:
    curve = CurveDomainParamter.get(req.publicKey.curve_name)
    is_valid = ecdsa.verify(
        req.publicKey.curve_name,
        Point(curve, int(req.publicKey.Q.x), int(req.publicKey.Q.y)),
        req.message,
        (int(req.signature.r), int(req.signature.s)),
    )
    return VerifyResponse(is_valid=is_valid)
