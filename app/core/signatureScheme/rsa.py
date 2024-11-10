from app.core.utils import inverse_mod, powermod, randomRelativePrime
from typing import Tuple
import hashlib


def generateKey(p: int, q: int) -> Tuple[int, int, int]:
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = randomRelativePrime(phi_n)
    d = inverse_mod(e, phi_n)
    return n, d, e


def H(message: str, n: int) -> int:
    return int(hashlib.sha512(message.encode()).hexdigest(), 16) % n


def sign(n: int, d: int, message: str) -> int:
    hashed_message = H(message, n)
    return powermod(hashed_message, d, n)


def verify(n: int, e: int, message: str, signature: int) -> bool:
    hash_message = H(message, n)
    return  hash_message == powermod(signature, e, n)
