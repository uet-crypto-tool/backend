import secrets
import multiprocessing
from typing import Tuple
from functools import partial
from app.core.ellipticCurve.point import Point
from app.core.ellipticCurve.domain import CurveDomainParamter
from app.core.ellipticCurve import Koblitz
from app.core.ellipticCurve.curve import Curve


def generateKey(curve_name: str, secret_number: int) -> Tuple[str, int, Point]:
    """
    Generate a public key for the given curve and secret number.

    Args:
        curve_name (str): The name of the elliptic curve to use.
        secret_number (int): The private key (secret number).

    Returns:
        Tuple[str, int, Point]: A tuple containing the curve name, secret number, and the corresponding public key (Point).
    """
    curve = CurveDomainParamter.get(curve_name)
    B = secret_number * curve.g
    return curve_name, secret_number, B


def encrypt(curve_name: str, B: Point, message: str) -> Tuple[Tuple[Point, Point]]:
    """
    Encrypt a message using elliptic curve encryption.

    Args:
        curve_name (str): The name of the elliptic curve to use.
        B (Point): The recipient's public key.
        message (str): The message to encrypt.

    Returns:
        Tuple[Tuple[Point, Point]]: A tuple of encrypted point pairs representing the encrypted message.
    """
    curve = CurveDomainParamter.get(curve_name)
    encoded_points, scale_factor = Koblitz.encode(
        message=message, curve_name=curve_name
    )

    # Encrypt each chunk of the message concurrently
    with multiprocessing.Pool() as pool:
        encrypted_pairs = pool.map(
            partial(encryptChunk, curve, B),
            (point for point in encoded_points),
        )

    return encrypted_pairs


def encryptChunk(curve: Curve, B: Point, M: Point) -> Tuple[Point, Point]:
    """
    Encrypt a single chunk of the message.

    Args:
        curve (Curve): The elliptic curve to use.
        B (Point): The recipient's public key.
        M (Point): The message point to encrypt.

    Returns:
        Tuple[Point, Point]: The encrypted point pair.
    """
    P = curve.g  # Base point of the curve
    k = secrets.randbits(8)  # Random value for encryption
    M1 = k * P  # First part of the ciphertext
    M2 = M + B * k  # Second part of the ciphertext
    return M1, M2


def decrypt(
    curve_name: str, secret_number: int, pair_points: Tuple[Tuple[Point, Point]]
) -> str:
    """
    Decrypt an encrypted message using the private key.

    Args:
        curve_name (str): The name of the elliptic curve to use.
        secret_number (int): The private key used for decryption.
        pair_points (Tuple[Tuple[Point, Point]]): The encrypted message represented as pairs of elliptic curve points.

    Returns:
        str: The decrypted message.
    """
    curve = CurveDomainParamter.get(curve_name)
    # Decrypt each chunk of the message concurrently
    with multiprocessing.Pool() as pool:
        decrypt_points = pool.map(
            partial(decryptChunk, curve, secret_number), pair_points
        )

    # Decode the decrypted points back to the original message
    decoded = Koblitz.decode(encoded_points=decrypt_points)
    return decoded


def decryptChunk(
    curve: Curve, secret_number: int, encrypted_message: Tuple[Point, Point]
) -> Point:
    """
    Decrypt a single chunk of the encrypted message.

    Args:
        curve (Curve): The elliptic curve to use.
        secret_number (int): The private key used for decryption.
        encrypted_message (Tuple[Point, Point]): A tuple representing the encrypted message to decrypt.

    Returns:
        Point: The decrypted point corresponding to the message chunk.
    """
    M1, M2 = map(lambda p: Point(curve, p.x, p.y), encrypted_message)
    M = M2 - M1 * secret_number  # Decrypt using the private key
    return M
