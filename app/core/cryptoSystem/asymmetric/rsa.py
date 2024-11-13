from app.core.utils import inverse_mod, powermod
from app.core.prime.generator import randomRelativePrime
from app.core.prime.primality import isPrime
from typing import Tuple


def generateKey(p: int, q: int, primality_check=False) -> Tuple[int, int, int]:
    """
    Generates an RSA key pair.

    Args:
        p (int): A prime number.
        q (int): Another prime number, distinct from p.

    Returns:
        Tuple[int, int, int]: (n, d, e) where:
            - n = p * q (modulus)
            - d = private key
            - e = public key

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
    d = randomRelativePrime(phi_n)
    e = inverse_mod(d, phi_n)
    return n, d, e


def encrypt(n: int, e: int, message: int) -> int:
    """
    Encrypts a message using RSA encryption.

    Args:
        n (int): The modulus (product of two primes).
        e (int): The public key.
        message (int): The plaintext message to encrypt.

    Returns:
        int: The encrypted message (ciphertext).

    Raises:
        ValueError: If the message is out of range.
    """
    if not (0 <= message < n):
        raise ValueError(f"Message must be in the range [0, {n - 1}].")

    return powermod(message, e, n)


def decrypt(n: int, d: int, encrypted_message: int) -> int:
    """
    Decrypts an RSA-encrypted message.

    Args:
        n (int): The modulus (product of two primes).
        d (int): The private key.
        encrypted_message (int): The ciphertext to decrypt.

    Returns:
        int: The decrypted plaintext message.

    Raises:
        ValueError: If the encrypted message is out of range.
    """
    if not (0 <= encrypted_message < n):
        raise ValueError(f"Encrypted message must be in the range [0, {n - 1}].")

    return powermod(encrypted_message, d, n)
