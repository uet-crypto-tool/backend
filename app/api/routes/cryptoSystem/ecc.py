from fastapi import APIRouter
from app.core.cryptoSystem import ecc
from app.schemas.ecc_schemas import (
    Seed,
    GenerateKeyResponse,
    EncryptRequest,
    EncryptResponse,
    DecryptRequest,
    DecryptResponse,
)

router = APIRouter()


@router.post("/ecc/generate_key", response_model=GenerateKeyResponse)
async def ecc_generate_key(seed: Seed):
    private_key, public_key = ecc.generateKey(seed)
    return GenerateKeyResponse(privateKey=private_key, publicKey=public_key)


@router.post("/ecc/encrypt", response_model=EncryptResponse)
async def ecc_encrypt(req: EncryptRequest) -> EncryptResponse:
    return EncryptResponse(encrypted_message=ecc.encrypt(req.publicKey, req.message))


@router.post("/ecc/decrypt", response_model=DecryptResponse)
async def ecc_decrypt(req: DecryptRequest) -> DecryptResponse:
    decrypted_message = ecc.decrypt(req.privateKey, req.encrypted_message)
    return DecryptResponse(decrypted_message=decrypted_message)
