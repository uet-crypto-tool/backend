import secrets
from typing import Tuple
from app.core.ellipticCurve.curve import Curve
from app.core.ellipticCurve.point import Point, PointType
from app.core.ellipticCurve.domain import CurveDomainParamter
from pydantic import BaseModel


class Seed(BaseModel):
    curve_domain_name: str


class PrivateKey(BaseModel):
    curve_domain_name: str
    s: int


class PublicKey(BaseModel):
    curve_domain_name: str
    B: PointType


def generateKeyOnDomain(curve_domain_name: str):
    return generateKey(CurveDomainParamter.create(curve_domain_name))


def generateKey(curve: Curve) -> Tuple[PrivateKey, PublicKey]:
    E = curve
    P = E.g
    s = secrets.randbits(1024)
    B = s * P
    return (
        PrivateKey(curve_domain_name=curve.name, s=s),
        PublicKey(curve_domain_name=curve.name, B=PointType(x=B.x, y=B.y))
    )


def encrypt(publicKey: PublicKey, M: PointType) -> Tuple[PointType, PointType]:
    E = CurveDomainParamter.create(publicKey.curve_domain_name)
    P = E.g

    B = publicKey.B
    B = Point(E, B.x, B.y)
    M = Point(E, M.x, M.y)

    k = secrets.randbits(8)
    M1 = k * P
    M2 = M + B * k
    return (M1.type(), M2.type())


def decrypt(privateKey: PrivateKey, encrypted_message: Tuple[PointType, PointType]) -> PointType:
    E = CurveDomainParamter.create(privateKey.curve_domain_name)
    M1, M2 = encrypted_message
    M1 = Point(E, M1.x, M1.y)
    M2 = Point(E, M2.x, M2.y)
    R = M2 - M1 * privateKey.s
    return R.type()
