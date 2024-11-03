from app.core.utils import inverse_mod, powermod, mul_mod, randomRelativePrime
from typing import Tuple
from app.schemas.elgamal_schemas import Seed, PrivateKey, PublicKey, Signature


def generateKey(seed: Seed) -> Tuple[PrivateKey, PublicKey]:
    p, a = seed.p, seed.a
    alpha = randomRelativePrime(p)
    beta = powermod(alpha, a, p)
    return (PrivateKey(p=p, a=a, alpha=alpha), PublicKey(p=p, alpha=alpha, beta=beta))


def H(message: int) -> int:
    return message


def sign(privateKey: PrivateKey, message: int) -> Signature:
    k = randomRelativePrime(privateKey.p - 1)
    y1 = powermod(privateKey.alpha, k, privateKey.p)

    ay1_mod = mul_mod(privateKey.a, y1, privateKey.p - 1)
    h_minus_ay1_mod = (H(message) - ay1_mod) % (privateKey.p - 1)
    k_inv = inverse_mod(k, privateKey.p - 1)
    y2 = mul_mod(h_minus_ay1_mod, k_inv, privateKey.p - 1)
    return Signature(y1=y1, y2=y2)


def verify(publicKey: PublicKey, message: int, signature: Signature) -> bool:
    y1, y2 = signature.y1, signature.y2
    v1 = mul_mod(
        powermod(publicKey.beta, y1, publicKey.p),
        powermod(y1, y2, publicKey.p),
        publicKey.p,
    )
    v2 = powermod(publicKey.alpha, H(message), publicKey.p)
    return v1 == v2
