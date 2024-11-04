from fastapi import APIRouter
from app.core.cryptoSystem import rsa
from app.schemas.rsa import (
    GenerateKeyResponse,
    EncryptRequest,
    EncryptResponse,
    DecryptRequest,
    DecryptResponse,
)

router = APIRouter()


@router.post("/rsa/generate_key", response_model=GenerateKeyResponse)
async def rsa_generate_key(seed: rsa.Seed):
    private_key, public_key = rsa.generateKey(seed)
    return GenerateKeyResponse(privateKey=private_key, publicKey=public_key)


@router.post("/rsa/encrypt", response_model=EncryptResponse)
async def rsa_encrypt(req: EncryptRequest) -> EncryptResponse:
    return EncryptResponse(encrypted_message=rsa.encrypt(req.publicKey, req.message))


@router.post("/rsa/decrypt", response_model=DecryptResponse)
async def rsa_decrypt(req: DecryptRequest) -> DecryptResponse:
    return DecryptResponse(
        decrypted_message=rsa.decrypt(req.privateKey, req.encrypted_message)
    )
