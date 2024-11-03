from fastapi import APIRouter
from app.core.cryptoSystem import elgamal
from app.schemas.elgamal_schemas import (
    GenerateKeyResponse,
    EncryptRequest,
    EncryptResponse,
    DecryptRequest,
    DecryptResponse,
)

router = APIRouter()


@router.post("/elgamal/generate_key", response_model=GenerateKeyResponse)
async def elgamal_generate_key(seed: elgamal.Seed):
    private_key, public_key = elgamal.generateKey(seed)
    return GenerateKeyResponse(privateKey=private_key, publicKey=public_key)


@router.post("/elgamal/encrypt", response_model=EncryptResponse)
async def elgamal_encrypt(
    req: EncryptRequest,
) -> EncryptResponse:
    return EncryptResponse(
        encrypted_message=elgamal.encrypt(req.publicKey, req.message)
    )


@router.post("/elgamal/decrypt", response_model=DecryptResponse)
async def elgamal_decrypt(
    req: DecryptRequest,
) -> DecryptResponse:
    return DecryptResponse(
        decrypted_message=elgamal.decrypt(req.privateKey, req.encrypted_message)
    )
