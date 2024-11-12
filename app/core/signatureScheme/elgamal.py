from app.core.utils import inverse_mod, powermod, mul_mod
from app.core.prime.generator import randomRelativePrime
from typing import Tuple
import hashlib


def generateKey(p: int, a: int) -> Tuple[int, int, int, int]:
    alpha = randomRelativePrime(p)
    beta = powermod(alpha, a, p)
    return p, a, alpha, beta


def H(message: str, n: int) -> int:
    return int(hashlib.sha512(message.encode()).hexdigest(), 16) % n


def sign(p: int, a: int, alpha: int, message: str) -> Tuple[int, int]:
    k = randomRelativePrime(p - 1)
    y1 = powermod(alpha, k, p)

    hashed_message = H(message, p)

    ay1_mod = mul_mod(a, y1, p - 1)
    h_minus_ay1_mod = (hashed_message - ay1_mod) % (p - 1)
    k_inv = inverse_mod(k, p - 1)
    y2 = mul_mod(h_minus_ay1_mod, k_inv, p - 1)
    return y1, y2


def verify(
    p: int, alpha: int, beta: int, message: str, signature: Tuple[int, int]
) -> bool:
    y1, y2 = signature
    hashed_message = H(message, p)

    v1 = mul_mod(
        powermod(beta, y1, p),
        powermod(y1, y2, p),
        p,
    )
    v2 = powermod(alpha, hashed_message, p)
    return v1 == v2
