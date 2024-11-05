from pydantic import BaseModel


class Seed(BaseModel):
    p: str
    q: str


class PublicKey(BaseModel):
    n: str
    e: str


class PrivateKey(BaseModel):
    n: str
    d: str


class GenerateKeyResponse(BaseModel):
    privateKey: PrivateKey
    publicKey: PublicKey


class EncryptedMessage(BaseModel):
    value: str


class EncryptRequest(BaseModel):
    publicKey: PublicKey
    message: str


class EncryptResponse(BaseModel):
    encrypted_message: EncryptedMessage


class DecryptRequest(BaseModel):
    privateKey: PrivateKey
    encrypted_message: EncryptedMessage


class DecryptResponse(BaseModel):
    decrypted_message: str


class Signature(BaseModel):
    value: str


class SignRequest(BaseModel):
    privateKey: PrivateKey
    message: str


class SignRespone(BaseModel):
    signature: Signature


class VerifyRequest(BaseModel):
    publicKey: PublicKey
    message: str
    signature: Signature


class VerifyResponse(BaseModel):
    is_valid: bool
