import secrets
import multiprocessing
from typing import Tuple
from functools import partial
from app.core.ellipticCurve.point import Point, PointType
from app.core.ellipticCurve.curve import Curve
from app.core.ellipticCurve.domain import CurveDomainParamter
from app.core.ellipticCurve import Koblitz
from pydantic import BaseModel


class Seed(BaseModel):
    curve_name: str


class PrivateKey(BaseModel):
    curve_name: str
    secret_number: int


class PublicKey(BaseModel):
    curve_name: str
    B: PointType


def generateKeyOnDomain(curve_name: str) -> Tuple[PrivateKey, PublicKey]:
    return generateKey(CurveDomainParamter.get(curve_name))


def generateKey(curve: Curve) -> Tuple[PrivateKey, PublicKey]:
    secret_number = secrets.randbits(1024)
    B = secret_number * curve.g
    return (
        PrivateKey(curve_name=curve.name, secret_number=secret_number),
        PublicKey(curve_name=curve.name, B=PointType(x=B.x, y=B.y)),
    )


def encryptPlainText(
    publicKey: PublicKey, message: str
) -> Tuple[Tuple[PointType, PointType]]:
    encoded_points, scale_factor = Koblitz.encode(
        message=message, curve_name=publicKey.curve_name
    )

    with multiprocessing.Pool() as pool:
        encrypted_pairs = pool.map(
            partial(encrypt, publicKey), (point.type() for point in encoded_points)
        )

    return encrypted_pairs


def encrypt(publicKey: PublicKey, M: PointType) -> Tuple[PointType, PointType]:
    curve = CurveDomainParamter.get(publicKey.curve_name)
    P = curve.g

    B = Point(curve, publicKey.B.x, publicKey.B.y)
    M = Point(curve, M.x, M.y)

    k = secrets.randbits(8)
    M1 = k * P
    M2 = M + B * k
    return (M1.type(), M2.type())


def decryptPlainText(
    privateKey: PrivateKey, encrypted_pairs: Tuple[Tuple[PointType, PointType]]
) -> str:

    with multiprocessing.Pool() as pool:
        decrypt_points = pool.map(partial(decrypt, privateKey), encrypted_pairs)

    curve = CurveDomainParamter.get(privateKey.curve_name)
    decrypt_points = [Point(curve, p.x, p.y) for p in decrypt_points]
    decoded = Koblitz.decode(encoded_points=decrypt_points)
    return decoded


def decrypt(
    privateKey: PrivateKey, encrypted_message: Tuple[PointType, PointType]
) -> PointType:
    curve = CurveDomainParamter.get(privateKey.curve_name)
    M1, M2 = map(lambda p: Point(curve, p.x, p.y), encrypted_message)
    M = M2 - M1 * privateKey.secret_number
    return M.type()
