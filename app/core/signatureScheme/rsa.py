from app.core.utils import inverse_mod, powermod, randomRelativePrime
from typing import Tuple


def generateKey(p: int, q: int) -> Tuple[int, int, int]:
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = randomRelativePrime(phi_n)
    d = inverse_mod(e, phi_n)
    return n, d, e


def H(m: int) -> int:
    return m


def sign(n: int, d: int, message: int) -> int:
    return powermod(H(message), d, n)


def verify(n: int, e: int, message: int, signature: int) -> bool:
    return H(message) == powermod(signature, e, n)
