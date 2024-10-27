import secrets
from typing import Tuple
from app.core.ellipticCurve.ellipticCurve import Curve, Point
from pydantic import BaseModel


class Seed(BaseModel):
    pass
    # curve: Curve
    # P: Point


class PrivateKey(BaseModel):
    s: int


class PublicKey(BaseModel):
    pass
    # E: Curve
    # P: Point
    # B: Point


def generateKeyOnDefinedCurve(curve_name: str):
    pass


def generateKey(self, curve: Curve, P: Point) -> Tuple[PrivateKey, PublicKey]:
    E = curve
    P = P
    s = secrets.randbits(2048)
    B = P * s
    return (PrivateKey(s=s), PublicKey(E=E, P=P, B=B))


def encrypt(publicKey: PublicKey, M: Point) -> Tuple[Point, Point]:
    k = secrets.randbits(2048)
    M1 = k * publicKey.P
    M2 = M + publicKey.B * k
    return (M1, M2)


def decrypt(privateKey: PrivateKey, M1: Point, M2: Point) -> Point:
    return M2 - M1 * privateKey.s
