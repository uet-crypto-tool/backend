from app.core.utils import inverse_mod, powermod, randomRelativePrime
from typing import Tuple


def generateKey(p: int, q: int) -> Tuple[int, int, int]:
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = randomRelativePrime(phi_n)
    e = inverse_mod(d, phi_n)
    return n, d, e


def encrypt(n: int, e: int, message: int) -> int:
    return powermod(message, e, n)


def decrypt(n: int, d: int, ecrypted_message: int) -> int:
    return powermod(ecrypted_message, d, n)
