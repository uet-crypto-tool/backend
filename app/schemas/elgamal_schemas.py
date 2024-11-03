from pydantic import BaseModel
from typing import Tuple


class Seed(BaseModel):
    p: int
    a: int


class PrivateKey(BaseModel):
    p: int
    a: int
    alpha: int


class PublicKey(BaseModel):
    p: int
    alpha: int
    beta: int


class GenerateKeyResponse(BaseModel):
    privateKey: PrivateKey
    publicKey: PublicKey


class EncryptedMessage(BaseModel):
    y1: int
    y2: int


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
    y1: int
    y2: int


class SignRequest(BaseModel):
    privateKey: PrivateKey
    message: int


class SignResponse(BaseModel):
    signature: Signature


class VerifyRequest(BaseModel):
    publicKey: PublicKey
    message: int
    signature: Signature


class VerifyResponse(BaseModel):
    is_valid: bool
