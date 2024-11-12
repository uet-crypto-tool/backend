import hashlib
from typing import Tuple
from app.core.utils import inverse_mod, powermod
from app.core.prime.generator import randomRelativePrime
from app.core.prime.primality import isPrime


def generateKey(p: int, q: int, primality_check=False) -> Tuple[int, int, int]:
    """
    Generates an RSA key pair.

    Args:
        p (int): A prime number.
        q (int): Another prime number, distinct from p.

    Returns:
        Tuple[int, int, int]: (n, d, e), where:
            - n: modulus (product of p and q)
            - d: private key (decryption key)
            - e: public key (encryption key)

    Raises:
        ValueError: If p and q are not distinct primes.
        ValueError: If p is not prime and `primality_check` is enabled.
        ValueError: If q is not prime and `primality_check` is enabled.
    """
    if p <= 1 or q <= 1:
        raise ValueError("p and q must be prime numbers greater than 1.")

    if primality_check:
        if not isPrime(p):
            raise ValueError("p primes.")
        if not isPrime(q):
            raise ValueError("q must be prime.")

    if p == q:
        raise ValueError("p and q must be distinct primes.")

    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Generate e as a random relative prime to φ(n)
    e = randomRelativePrime(phi_n)
    # Compute d, the modular inverse of e modulo φ(n)
    d = inverse_mod(e, phi_n)

    return n, d, e


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

    hashed = hashlib.sha512(message.encode()).hexdigest()
    return int(hashed, 16) % n


def sign(n: int, d: int, message: str) -> int:
    """
    Signs a message using the private key.

    Args:
        n (int): The modulus.
        d (int): The private key.
        message (str): The message to sign.

    Returns:
        int: The digital signature.
    """
    if n <= 0 or d <= 0:
        raise ValueError("n and d must be positive integers.")

    hashed_message = H(message, n)
    return powermod(hashed_message, d, n)


def verify(n: int, e: int, message: str, signature: int) -> bool:
    """
    Verifies a digital signature.

    Args:
        n (int): The modulus.
        e (int): The public key.
        message (str): The original message.
        signature (int): The digital signature.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    if n <= 0 or e <= 0 or signature < 0:
        raise ValueError(
            "n and e must be positive integers, and the signature must be non-negative."
        )

    hashed_message = H(message, n)
    recovered_hash = powermod(signature, e, n)
    return hashed_message == recovered_hash
