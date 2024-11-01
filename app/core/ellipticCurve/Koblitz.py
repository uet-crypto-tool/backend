import multiprocessing
from typing import Tuple
from functools import partial

from app.core.ellipticCurve.point import Point
from app.core.ellipticCurve.domain import CurveDomainParamter


def encodeChunk(
        message: str,
        curve_name: str = "secp521r1",
        d: int = 100,
        chunk_size: int = 10,
        alphabet_size: int = 2**8
) -> Tuple[Point]:
    curve = CurveDomainParamter.get(curve_name=curve_name)
    message_decimal = sum(
        ord(char) * (alphabet_size**i) for i, char in enumerate(message[:chunk_size])
    )

    for j in range(1, d - 1):
        x = (d * message_decimal + j) % curve.p
        s = (x**3 + curve.a * x + curve.b) % curve.p

        if s == pow(s, (curve.p + 1) // 2, curve.p):
            y = pow(s, (curve.p + 1) // 4, curve.p)

            if curve.on_curve(x, y):
                break

    return Point(curve, x, y)


def encode(
        message: str,
        curve_name: str = "secp521r1",
        d: int = 100,
        chunk_size: int = 10,
        alphabet_size: int = 2**8
) -> Tuple[Tuple[Point], int]:
    pool = multiprocessing.Pool()
    encoded_messages = pool.map(
        partial(encodeChunk, curve_name=curve_name, d=d,
                alphabet_size=alphabet_size, chunk_size=chunk_size),
        [message[i: i + chunk_size]
            for i in range(0, len(message), chunk_size)],
    )
    pool.close()
    pool.join()

    return tuple(encoded_messages), d


def decodeSinglePoint(
    encoded: Point,
    d: int = 100,
    alphabet_size: int = 2**8,
) -> str:
    message_decimal = encoded.x // d

    characters = []
    while message_decimal != 0:
        characters.append(chr(message_decimal % alphabet_size))
        message_decimal //= alphabet_size

    return "".join(characters)


def decode(
    encoded: Tuple[Tuple[Point], int],
    alphabet_size: int = 2**8,
) -> str:
    encoded_points, d = encoded

    pool = multiprocessing.Pool()
    characters = []
    characters = pool.starmap(
        partial(decodeSinglePoint, d=d, alphabet_size=alphabet_size),
        [(point, ) for point in encoded_points],
    )
    pool.close()
    pool.join()

    return "".join(characters)
