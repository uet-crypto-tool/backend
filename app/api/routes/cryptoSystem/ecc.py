from fastapi import APIRouter
from app.core.cryptoSystem.asymmetric import ecc
from app.core.ellipticCurve.domain import CurveDomainParamter
from app.core.ellipticCurve.point import Point
from app.schemas.ecc import (
    Seed,
    PrivateKey,
    PublicKey,
    GenerateKeyResponse,
    EncryptRequest,
    EncryptedMessage,
    EncryptResponse,
    DecryptRequest,
    DecryptResponse,
)

router = APIRouter()


@router.post("/ecc/generate_key", response_model=GenerateKeyResponse)
async def ecc_generate_key(seed: Seed):
    curve_name, secret_number, B = ecc.generateKey(
        seed.curve_name, int(seed.secret_number)
    )
    return GenerateKeyResponse(
        privateKey=PrivateKey(curve_name=curve_name, secret_number=str(secret_number)),
        publicKey=PublicKey(curve_name=curve_name, B=B.type()),
    )


@router.post("/ecc/encrypt", response_model=EncryptResponse)
async def ecc_encrypt(req: EncryptRequest) -> EncryptResponse:
    curve = CurveDomainParamter.get(
        req.publicKey.curve_name,
    )
    encrypted_pairs = ecc.encrypt(
        req.publicKey.curve_name,
        Point(curve, req.publicKey.B.x, req.publicKey.B.y),
        req.message,
    )
    encrypted_pairs = [(pair[0].type(), pair[1].type()) for pair in encrypted_pairs]
    return EncryptResponse(
        encrypted_message=EncryptedMessage(pair_points=encrypted_pairs)
    )


@router.post("/ecc/decrypt", response_model=DecryptResponse)
async def ecc_decrypt(req: DecryptRequest) -> DecryptResponse:
    curve = CurveDomainParamter.get(req.privateKey.curve_name)
    pair_points = [
        (Point(curve, pair[0].x, pair[0].y), Point(curve, pair[1].x, pair[1].y))
        for pair in req.encrypted_message.pair_points
    ]
    decrypted_message = ecc.decrypt(
        req.privateKey.curve_name, int(req.privateKey.secret_number), pair_points
    )
    return DecryptResponse(decrypted_message=decrypted_message)
