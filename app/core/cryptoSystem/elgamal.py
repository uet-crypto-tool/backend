from app.core.utils import powermod, mul_mod, randomIntInRange
from app.core.prime.generator import randomRelativePrime
from app.core.prime.primality import isPrime
from typing import Tuple


def generateKey(
    p: int, a: int, primality_check: bool = False
) -> Tuple[int, int, int, int]:
    """
    Generates a cryptographic key pair for ElGamal encryption.

    Args:
        p (int): A prime modulus.
        a (int): The private key (randomly chosen).
        primality_check (bool): If True, verify that p is a prime number.

    Returns:
        Tuple[int, int, int, int]: (p, a, alpha, beta) where:
            - p: The prime modulus.
            - a: The private key.
            - alpha: The generator of the group.
            - beta: The public key component (beta = alpha^a mod p).

    Raises:
        ValueError: If p is not prime and `primality_check` is enabled.
    """
    if primality_check and not isPrime(p):
        raise ValueError("The modulus p must be a prime number.")

    alpha = randomRelativePrime(p)  # Generator of the group
    beta = powermod(alpha, a, p)  # Public key component

    return p, a, alpha, beta


def encrypt(
    p: int, alpha: int, beta: int, message: int, primality_check=False
) -> Tuple[int, int]:
    """
    Encrypts a message using the ElGamal encryption scheme.

    Args:
        p (int): The prime modulus.
        alpha (int): The generator of the group.
        beta (int): The public key component.
        message (int): The plaintext message to encrypt.

    Returns:
            - y2 = message * beta^k mod p
    """
    if not (0 <= message < p):
        raise ValueError(f"Message must be in the range [0, {p - 1}].")

    if primality_check and not isPrime(p):
        raise ValueError("The modulus p must be a prime number.")

    k = randomIntInRange(1, p - 1)  # Random ephemeral key
    y1 = powermod(alpha, k, p)
    y2 = mul_mod(message, powermod(beta, k, p), p)

    return y1, y2


def decrypt(
    p: int, a: int, encrypted_message: Tuple[int, int], primality_check=False
) -> int:
    """
    Decrypts a message encrypted with the ElGamal encryption scheme.

    Args:
        p (int): The prime modulus.
        a (int): The private key.
        encrypted_message (Tuple[int, int]): The ciphertext (y1, y2).

    Returns:
        int: The decrypted plaintext message.
    """

    if primality_check and not isPrime(p):
        raise ValueError("The modulus p must be a prime number.")

    y1, y2 = encrypted_message

    # Compute the modular inverse of y1^a mod p
    y1_a_inverse = powermod(y1, p - 1 - a, p)  # Equivalent to y1^-a mod p
    decrypted_message = mul_mod(y2, y1_a_inverse, p)

    return decrypted_message

    return decrypted_message
