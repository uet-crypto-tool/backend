from pydantic import BaseModel


class Seed(BaseModel):
    p: int
    q: int


class PublicKey(BaseModel):
    n: int
    e: int


class PrivateKey(BaseModel):
    n: int
    d: int


class GenerateKeyResponse(BaseModel):
    privateKey: PrivateKey
    publicKey: PublicKey


class EncryptedMessage(BaseModel):
    value: int


class EncryptRequest(BaseModel):
    publicKey: PublicKey
    message: int


class EncryptResponse(BaseModel):
    encrypted_message: EncryptedMessage


class DecryptRequest(BaseModel):
    privateKey: PrivateKey
    encrypted_message: EncryptedMessage


class DecryptResponse(BaseModel):
    decrypted_message: int


class Signature(BaseModel):
    value: int


class SignRequest(BaseModel):
    privateKey: PrivateKey
    message: int


class SignRespone(BaseModel):
    signature: Signature


class VerifyRequest(BaseModel):
    publicKey: PublicKey
    message: int
    signature: Signature


class VerifyResponse(BaseModel):
    is_valid: bool
