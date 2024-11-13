from fastapi import APIRouter
from app.core.cryptoSystem.asymmetric import elgamal
from app.schemas.elgamal import (
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


@router.post("/elgamal/generate_key", response_model=GenerateKeyResponse)
async def elgamal_generate_key(seed: Seed):
    p, a, alpha, beta = elgamal.generateKey(int(seed.p), int(seed.a))
    privateKey = PrivateKey(p=str(p), a=str(a), alpha=str(alpha))
    publicKey = PublicKey(p=str(p), alpha=str(alpha), beta=str(beta))
    return GenerateKeyResponse(privateKey=privateKey, publicKey=publicKey)


@router.post("/elgamal/encrypt", response_model=EncryptResponse)
async def elgamal_encrypt(
    req: EncryptRequest,
) -> EncryptResponse:
    y1, y2 = elgamal.encrypt(
        int(req.publicKey.p),
        int(req.publicKey.alpha),
        int(req.publicKey.beta),
        int(req.message),
    )
    return EncryptResponse(encrypted_message=EncryptedMessage(y1=str(y1), y2=str(y2)))


@router.post("/elgamal/decrypt", response_model=DecryptResponse)
async def elgamal_decrypt(
    req: DecryptRequest,
) -> DecryptResponse:
    decrypted_message = elgamal.decrypt(
        int(req.privateKey.p),
        int(req.privateKey.a),
        (int(req.encrypted_message.y1), int(req.encrypted_message.y2)),
    )
    return DecryptResponse(decrypted_message=str(decrypted_message))
