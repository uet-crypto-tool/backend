from fastapi import APIRouter
from app.core.cryptoSystem import rsa
from pydantic import BaseModel

router = APIRouter()


class GenerateKeyResponse(BaseModel):
    privateKey: rsa.PrivateKey
    publicKey: rsa.PublicKey


class EncryptRequest(BaseModel):
    publicKey: rsa.PublicKey
    message: int


class EncryptResponse(BaseModel):
    encrypted_message: int


class DecryptRequest(BaseModel):
    privateKey: rsa.PrivateKey
    encrypted_message: int


class DecryptResponse(BaseModel):
    decrypted_message: int


@router.post("/rsa/generate_key", response_model=GenerateKeyResponse)
async def rsa_generate_key(seed: rsa.Seed):
    private_key, public_key = rsa.generateKey(seed)
    return {"privateKey": private_key, "publicKey": public_key}


@router.post("/rsa/encrypt", response_model=EncryptResponse)
async def rsa_encrypt(req: EncryptRequest) -> EncryptResponse:
    return EncryptResponse(encrypted_message=rsa.encrypt(req.publicKey, req.message))


@router.post("/rsa/decrypt", response_model=DecryptResponse)
async def rsa_decrypt(req: DecryptRequest) -> DecryptResponse:
    return DecryptResponse(
        decrypted_message=rsa.decrypt(req.privateKey, req.encrypted_message)
    )
