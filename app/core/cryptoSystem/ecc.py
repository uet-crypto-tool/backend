import secrets
import multiprocessing
from typing import Tuple
from functools import partial
from app.core.ellipticCurve.point import Point
from app.core.ellipticCurve.domain import CurveDomainParamter
from app.core.ellipticCurve import Koblitz
from app.core.ellipticCurve.curve import Curve


def generateKey(curve_name: str, secret_number: int) -> Tuple[str, int, Point]:
    curve = CurveDomainParamter.get(curve_name)
    B = secret_number * curve.g
    return curve_name, secret_number, B


def encrypt(curve_name: int, B: Point, message: str) -> Tuple[Tuple[Point, Point]]:
    curve = CurveDomainParamter.get(curve_name)
    encoded_points, scale_factor = Koblitz.encode(
        message=message, curve_name=curve_name
    )

    with multiprocessing.Pool() as pool:
        encrypted_pairs = pool.map(
            partial(encryptChunk, curve, B),
            (point for point in encoded_points),
        )

    return encrypted_pairs


def encryptChunk(curve: Curve, B: Point, M: Point) -> Tuple[Point, Point]:
    P = curve.g
    k = secrets.randbits(8)
    M1 = k * P
    M2 = M + B * k
    return M1, M2


def decrypt(
    curve_name: str, secret_number: int, pair_points: Tuple[Tuple[Point, Point]]
) -> str:

    curve = CurveDomainParamter.get(curve_name)
    with multiprocessing.Pool() as pool:
        decrypt_points = pool.map(
            partial(decryptChunk, curve, secret_number), pair_points
        )

    decoded = Koblitz.decode(encoded_points=decrypt_points)
    return decoded


def decryptChunk(
    curve: Curve, secret_number, encrypted_message: Tuple[Point, Point]
) -> Point:
    M1, M2 = map(lambda p: Point(curve, p.x, p.y), encrypted_message)
    M = M2 - M1 * secret_number
    return M
