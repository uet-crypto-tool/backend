from pydantic import BaseModel
from typing import Tuple
from app.core.ellipticCurve.point import PointType


class Seed(BaseModel):
    curve_name: str


class PublicKey(BaseModel):
    curve_name: str
    Q: PointType


class PrivateKey(BaseModel):
    curve_name: str
    d: int


class GenerateKeyResponse(BaseModel):
    privateKey: PrivateKey
    publicKey: PublicKey


class Signature(BaseModel):
    r: int
    s: int


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
