from app.core.utils import inverse_mod, powermod, mul_mod, randomRelativePrime
from typing import Tuple
from app.schemas.elgamal import Seed, PrivateKey, PublicKey, Signature


def generateKey(p: int, a: int) -> Tuple[int, int, int, int]:
    alpha = randomRelativePrime(p)
    beta = powermod(alpha, a, p)
    return p, a, alpha, beta


def H(message: int) -> int:
    return message


def sign(p: int, a: int, alpha: int, message: int) -> Tuple[int, int]:
    k = randomRelativePrime(p - 1)
    y1 = powermod(alpha, k, p)

    ay1_mod = mul_mod(a, y1, p - 1)
    h_minus_ay1_mod = (H(message) - ay1_mod) % (p - 1)
    k_inv = inverse_mod(k, p - 1)
    y2 = mul_mod(h_minus_ay1_mod, k_inv, p - 1)
    return y1, y2


def verify(
    p: int, alpha: int, beta: int, message: int, signature: Tuple[int, int]
) -> bool:
    y1, y2 = signature
    v1 = mul_mod(
        powermod(beta, y1, p),
        powermod(y1, y2, p),
        p,
    )
    v2 = powermod(alpha, H(message), p)
    return v1 == v2
