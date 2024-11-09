from app.core.utils import powermod, mul_mod, randomRelativePrime, randomIntInRange
from typing import Tuple


def generateKey(p: int, a: int) -> Tuple[int, int, int, int]:
    alpha = randomRelativePrime(p)
    beta = powermod(alpha, a, p)
    return p, a, alpha, beta


def encrypt(p: int, alpha: int, beta: int, message: int) -> Tuple[int, int]:
    k = randomIntInRange(1, p - 1)
    y1 = powermod(alpha, k, p)
    y2 = mul_mod(message, powermod(beta, k, p), p)
    return y1, y2


def decrypt(p: int, a: int, encrypted_message: Tuple[int, int]) -> int:
    y1, y2 = encrypted_message
    return mul_mod(y2, powermod(y1, -a, p), p)
