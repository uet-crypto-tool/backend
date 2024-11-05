from pydantic import BaseModel
from typing import Tuple
from app.core.ellipticCurve.point import PointType


class Seed(BaseModel):
    curve_name: str
    secret_number: str


class PrivateKey(BaseModel):
    curve_name: str
    secret_number: str


class PublicKey(BaseModel):
    curve_name: str
    B: PointType


class GenerateKeyResponse(BaseModel):
    privateKey: PrivateKey
    publicKey: PublicKey


class EncryptedMessage(BaseModel):
    pair_points: Tuple[Tuple[PointType, PointType], ...]


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
