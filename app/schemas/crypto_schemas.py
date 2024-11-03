from app.core.cryptoSystem import rsa
from pydantic import BaseModel


class RSAGenerateKeyResponse(BaseModel):
    privateKey: rsa.PrivateKey
    publicKey: rsa.PublicKey


class RSAEncryptRequest(BaseModel):
    publicKey: rsa.PublicKey
    message: int


class EncryptResponse(BaseModel):
    encrypted_message: int


class RSADecryptRequest(BaseModel):
    privateKey: rsa.PrivateKey
    encrypted_message: int


class RSADecryptResponse(BaseModel):
    decrypted_message: int
