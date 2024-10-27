from fastapi import APIRouter
from app.core.cryptoSystem import rsa
from pydantic import BaseModel

router = APIRouter()


@router.post("/rsa/generate_key")
async def rsa_generate_key(seed: rsa.Seed):
    private_key, public_key = rsa.generateKey(seed)
    return {
        "privateKey": private_key,
        "publicKey": public_key
    }


class RSA_EncryptRequest(BaseModel):
    publicKey: rsa.PublicKey
    message: int


@router.post("/rsa/encrypt")
async def rsa_encrypt(req: RSA_EncryptRequest):
    return rsa.encrypt(req.publicKey, req.message)


class RSA_DecryptRequest(BaseModel):
    privateKey: rsa.PrivateKey
    encrypted_message: int


@router.post("/rsa/decrypt")
async def rsa_decrypt(req: RSA_DecryptRequest):
    return rsa.decrypt(req.privateKey, req.encrypted_message)
