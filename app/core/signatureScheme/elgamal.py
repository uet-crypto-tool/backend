from app.core.utils import inverse_mod, powermod, mul_mod
from app.core.prime.generator import randomRelativePrime
from app.core.prime.primality import isPrime
from typing import Tuple
import hashlib


def generateKey(
    p: int, a: int, primality_check: bool = False
) -> Tuple[int, int, int, int]:
    """
    Generates a digital signature key pair.

    Args:
        p (int): A prime modulus.
        a (int): The private signing key.

    Returns:
        Tuple[int, int, int, int]: (p, a, alpha, beta), where:
            - p: The prime modulus.
            - a: The private signing key.
            - alpha: The generator of the group.
            - beta: The public verification key (beta = alpha^a mod p).
    """
    if p <= 1:
        raise ValueError("p must be a prime number greater than 1.")

    if a <= 0 or a >= p - 1:
        raise ValueError(f"a must be in the range [1, {p - 2}].")

    if primality_check and not isPrime(p):
        raise ValueError("The modulus p must be a prime number.")

    alpha = randomRelativePrime(p)
    beta = powermod(alpha, a, p)
    return p, a, alpha, beta


def H(message: str, n: int) -> int:
    """
    Hashes a message using SHA-512 and reduces it modulo n.

    Args:
        message (str): The message to hash.
        n (int): The modulus for reduction.

    Returns:
        int: The hashed and reduced message.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer.")

    return int(hashlib.sha512(message.encode()).hexdigest(), 16) % n


def sign(
    p: int, a: int, alpha: int, message: str, primality_check: bool = False
) -> Tuple[int, int]:
    """
    Signs a message using the ElGamal signature scheme.

    Args:
        p (int): The prime modulus.
        a (int): The private signing key.
        alpha (int): The generator of the group.
        message (str): The message to sign.

    Returns:
        Tuple[int, int]: The signature (y1, y2), where:
            - y1 = alpha^k mod p
            - y2 = (H(message) - a * y1) * k^-1 mod (p - 1)
    """
    if p <= 1:
        raise ValueError("p must be a prime number greater than 1.")

    if primality_check and not isPrime(p):
        raise ValueError("The modulus p must be a prime number.")

    k = randomRelativePrime(p - 1)
    y1 = powermod(alpha, k, p)

    hashed_message = H(message, p)

    ay1_mod = mul_mod(a, y1, p - 1)
    h_minus_ay1_mod = (hashed_message - ay1_mod) % (p - 1)
    k_inv = inverse_mod(k, p - 1)
    y2 = mul_mod(h_minus_ay1_mod, k_inv, p - 1)
    return y1, y2


def verify(
    p: int,
    alpha: int,
    beta: int,
    message: str,
    signature: Tuple[int, int],
    primality_check: bool = False,
) -> bool:
    """
    Verifies an ElGamal signature.

    Args:
        p (int): The prime modulus.
        alpha (int): The generator of the group.
        beta (int): The public verification key.
        message (str): The original message.
        signature (Tuple[int, int]): The signature (y1, y2).

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    if p <= 1:
        raise ValueError("p must be a prime number greater than 1.")

    if primality_check and not isPrime(p):
        raise ValueError("The modulus p must be a prime number.")

    y1, y2 = signature
    hashed_message = H(message, p)

    v1 = mul_mod(
        powermod(beta, y1, p),
        powermod(y1, y2, p),
        p,
    )
    v2 = powermod(alpha, hashed_message, p)
    return v1 == v2
