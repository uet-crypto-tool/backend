from app.core.ellipticCurve.domain import CurveDomainParamter
from app.core.ellipticCurve.point import Point
from app.core.utils import inverse_mod, mul_mod, randomIntInRange
from typing import Tuple
import hashlib


def generateKey(curve_name: str) -> Tuple[str, int, Point]:
    """
    Generate a key pair for the given elliptic curve.

    Args:
        curve_name (str): The name of the elliptic curve.

    Returns:
        Tuple[str, int, Point]: The curve name, private key (d), and public key (Q).
    """
    curve = CurveDomainParamter.get(curve_name)
    d = randomIntInRange(1, curve.n - 1)  # Private key
    Q = curve.g * d  # Public key
    return curve_name, d, Q


def H(message: str, n: int) -> int:
    """
    Hash the message and reduce it modulo n.

    Args:
        message (str): The message to hash.
        n (int): The modulus for the hash.

    Returns:
        int: The hashed message modulo n.
    """
    return int(hashlib.sha512(message.encode()).hexdigest(), 16) % n


def sign(curve_name: str, d: int, message: str) -> Tuple[int, int]:
    """
    Generate a digital signature for a given message.

    Args:
        curve_name (str): The name of the elliptic curve.
        d (int): The private key.
        message (str): The message to sign.

    Returns:
        Tuple[int, int]: The signature as a tuple (r, s).
    """
    curve = CurveDomainParamter.get(curve_name)
    G = curve.g
    n = curve.n

    while True:
        k = randomIntInRange(1, n - 1)  # Ephemeral private key
        x = (G * k).x  # x-coordinate of kG
        r = x % n
        if r == 0:
            continue

        hashed_message = H(message, n)
        dr_mod_n = mul_mod(d, r, n)
        h_plus_dr_mod_n = (hashed_message + dr_mod_n) % n
        k_inv = inverse_mod(k, n)
        s = mul_mod(h_plus_dr_mod_n, k_inv, n)
        if s != 0:
            break

    return r, s


def verify(curve_name: str, Q: Point, message: str, signature: Tuple[int, int]) -> bool:
    """
    Verify a digital signature.

    Args:
        curve_name (str): The name of the elliptic curve.
        Q (Point): The public key.
        message (str): The message to verify.
        signature (Tuple[int, int]): The signature as a tuple (r, s).

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    curve = CurveDomainParamter.get(curve_name)
    G = curve.g
    r, s = signature

    if not (1 <= r < curve.n and 1 <= s < curve.n):
        return False  # Invalid signature

    n = curve.n
    w = inverse_mod(s, n)  # Compute w = s^(-1) mod n
    h = H(message, n)
    u1 = mul_mod(h, w, n)
    u2 = mul_mod(r, w, n)

    # Compute v = (u1 * G + u2 * Q).x mod n
    point_result = G * u1 + Q * u2
    v = point_result.x % n
    return v == r
