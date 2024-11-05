from pydantic import BaseModel
from typing import Tuple


class Seed(BaseModel):
    p: str
    a: str


class PrivateKey(BaseModel):
    p: str
    a: str
    alpha: str


class PublicKey(BaseModel):
    p: str
    alpha: str
    beta: str


class GenerateKeyResponse(BaseModel):
    privateKey: PrivateKey
    publicKey: PublicKey


class EncryptedMessage(BaseModel):
    y1: str
    y2: str


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
    y1: str
    y2: str


class SignRequest(BaseModel):
    privateKey: PrivateKey
    message: str


class SignResponse(BaseModel):
    signature: Signature


class VerifyRequest(BaseModel):
    publicKey: PublicKey
    message: str
    signature: Signature


class VerifyResponse(BaseModel):
    is_valid: bool
