from app.core.utils import inverse_mod, powermod, randomRelativePrime
from typing import Tuple
from app.schemas.rsa import Seed, PublicKey, PrivateKey, Signature


def generateKey(seed: Seed) -> Tuple[PrivateKey, PublicKey]:
    p, q = seed.p, seed.q
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = randomRelativePrime(phi_n)
    d = inverse_mod(e, phi_n)
    return (PrivateKey(n=n, d=e), PublicKey(n=n, e=d))


def H(m: int) -> int:
    return m


def sign(privateKey: PrivateKey, message: int) -> Signature:
    return Signature(value=powermod(H(message), privateKey.d, privateKey.n))


def verify(publicKey: PublicKey, message: int, signature: Signature) -> bool:
    return H(message) == powermod(signature.value, publicKey.e, publicKey.n)
