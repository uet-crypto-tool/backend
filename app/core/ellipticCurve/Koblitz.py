import multiprocessing
from typing import Tuple
from functools import partial

from app.core.ellipticCurve.point import Point
from app.core.utils import powermod, encodeString, decodeString
from app.core.ellipticCurve.domain import CurveDomainParamter
from app.core.ellipticCurve.curve import Curve


def getPointOnCurve(message_decimal: int, curve: Curve, scale_factor: int):
    """
    Maps a message (as a decimal integer) to a point on the elliptic curve.

    Args:
        message_decimal (int): The message represented as a decimal number.
        curve (Curve): The elliptic curve.
        scale_factor (int): The scaling factor.

    Returns:
        Point: A valid point on the elliptic curve.

    Raises:
        ValueError: If no valid point can be found on the curve.
    """

    for j in range(1, scale_factor - 1):
        x = (scale_factor * message_decimal + j) % curve.p
        s = (x**3 + curve.a * x + curve.b) % curve.p

        if s == powermod(s, (curve.p + 1) // 2, curve.p):
            y = powermod(s, (curve.p + 1) // 4, curve.p)

            if curve.on_curve(x, y):
                return Point(curve, x, y)

    raise ValueError("Could not find a valid point on the curve.")


def encodeChunk(
    message: str,
    curve_name: str = "secp521r1",
    scale_factor: int = 100,
    alphabet_size: int = 2**8,
) -> Tuple[Point]:
    """
    Encodes a single chunk of the message into elliptic curve points.

    Args:
        chunk (str): The chunk of the message to encode.
        curve (Curve): The elliptic curve used for encoding.
        scale_factor (int): The scaling factor.
        alphabet_size (int): The size of the encoding alphabet.

    Returns:
        Tuple[Point, ...]: The encoded points corresponding to the chunk.
    """
    curve = CurveDomainParamter.get(curve_name=curve_name)
    message_decimal = encodeString(message, alphabet_size)
    return getPointOnCurve(message_decimal, curve, scale_factor)


def encode(
    message: str,
    curve_name: str = "secp521r1",
    scale_factor: int = 100,
    chunk_size: int = 10,
    alphabet_size: int = 2**8,
) -> Tuple[Tuple[Point], int]:
    """
    Encodes a message into elliptic curve points.

    Args:
        message (str): The message to encode.
        curve_name (str): The name of the elliptic curve to use.
        scale_factor (int): The scaling factor.
        chunk_size (int): The size of message chunks.
        alphabet_size (int): The size of the encoding alphabet.

    Returns:
        Tuple[List[Point], int]: A list of encoded points and the scale factor.
    """
    with multiprocessing.Pool() as pool:
        encoded_messages = pool.map(
            partial(
                encodeChunk,
                curve_name=curve_name,
                scale_factor=scale_factor,
                alphabet_size=alphabet_size,
            ),
            (message[i : i + chunk_size] for i in range(0, len(message), chunk_size)),
        )

    return encoded_messages, scale_factor


def decodeSinglePoint(
    encoded: Point,
    scale_factor: int = 100,
    alphabet_size: int = 2**8,
) -> str:
    """
    Decodes a single elliptic curve point into a character.

    Args:
        encoded (Point): The elliptic curve point to decode.
        scale_factor (int): The scaling factor.
        alphabet_size (int): The size of the decoding alphabet.

    Returns:
        str: The decoded character.
    """
    return decodeString(encoded.x // scale_factor)


def decode(
    encoded_points: Tuple[Point],
    scale_factor: int = 100,
    alphabet_size: int = 2**8,
) -> str:
    """
    Decodes a list of elliptic curve points back into a message.

    Args:
        encoded_points (List[Point]): The encoded points.
        scale_factor (int): The scaling factor.
        alphabet_size (int): The size of the decoding alphabet.

    Returns:
        str: The decoded message.
    """
    with multiprocessing.Pool() as pool:
        characters = pool.starmap(
            partial(
                decodeSinglePoint,
                scale_factor=scale_factor,
                alphabet_size=alphabet_size,
            ),
            [(point,) for point in encoded_points],
        )

    return "".join(characters)
