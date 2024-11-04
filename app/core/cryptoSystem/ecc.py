import secrets
import multiprocessing
from typing import Tuple
from functools import partial
from app.core.ellipticCurve.point import Point, PointType
from app.core.ellipticCurve.domain import CurveDomainParamter
from app.core.ellipticCurve import Koblitz
from app.schemas.ecc import Seed, PrivateKey, PublicKey, EncryptedMessage


def generateKey(seed: Seed) -> Tuple[PrivateKey, PublicKey]:
    curve = CurveDomainParamter.get(seed.curve_name)
    secret_number = secrets.randbits(1024)
    B = secret_number * curve.g
    return (
        PrivateKey(curve_name=curve.name, secret_number=secret_number),
        PublicKey(curve_name=curve.name, B=PointType(x=B.x, y=B.y)),
    )


def encrypt(publicKey: PublicKey, message: str) -> EncryptedMessage:
    encoded_points, scale_factor = Koblitz.encode(
        message=message, curve_name=publicKey.curve_name
    )

    with multiprocessing.Pool() as pool:
        encrypted_pairs = pool.map(
            partial(encryptChunk, publicKey), (point.type() for point in encoded_points)
        )

    return EncryptedMessage(pair_points=encrypted_pairs)


def encryptChunk(publicKey: PublicKey, M: PointType) -> Tuple[PointType, PointType]:
    curve = CurveDomainParamter.get(publicKey.curve_name)
    P = curve.g

    B = Point(curve, publicKey.B.x, publicKey.B.y)
    M = Point(curve, M.x, M.y)

    k = secrets.randbits(8)
    M1 = k * P
    M2 = M + B * k
    return (M1.type(), M2.type())


def decrypt(privateKey: PrivateKey, encryptedMessage: EncryptedMessage) -> str:

    with multiprocessing.Pool() as pool:
        decrypt_points = pool.map(
            partial(decryptChunk, privateKey), encryptedMessage.pair_points
        )

    curve = CurveDomainParamter.get(privateKey.curve_name)
    decrypt_points = [Point(curve, p.x, p.y) for p in decrypt_points]
    decoded = Koblitz.decode(encoded_points=decrypt_points)
    return decoded


def decryptChunk(
    privateKey: PrivateKey, encrypted_message: Tuple[PointType, PointType]
) -> PointType:
    curve = CurveDomainParamter.get(privateKey.curve_name)
    M1, M2 = map(lambda p: Point(curve, p.x, p.y), encrypted_message)
    M = M2 - M1 * privateKey.secret_number
    return M.type()
