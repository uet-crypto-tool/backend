from fastapi import APIRouter
from app.core.cryptoSystem.asymmetric import rsa
from app.schemas.rsa import (
    Seed,
    GenerateKeyResponse,
    EncryptRequest,
    EncryptedMessage,
    EncryptResponse,
    DecryptRequest,
    DecryptResponse,
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


@router.post("/rsa/encrypt", response_model=EncryptResponse)
async def rsa_encrypt(req: EncryptRequest) -> EncryptResponse:
    encrypted_message = EncryptedMessage(
        value=str(
            rsa.encrypt(int(req.publicKey.n), int(req.publicKey.e), int(req.message))
        )
    )
    return EncryptResponse(encrypted_message=encrypted_message)


@router.post("/rsa/decrypt", response_model=DecryptResponse)
async def rsa_decrypt(req: DecryptRequest) -> DecryptResponse:
    decrypted_message = rsa.decrypt(
        int(req.privateKey.n), int(req.privateKey.d), int(req.encrypted_message.value)
    )
    return DecryptResponse(decrypted_message=str(decrypted_message))
