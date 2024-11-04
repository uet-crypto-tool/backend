from app.core.utils import inverse_mod, powermod, randomRelativePrime
from app.schemas.rsa import Seed, PublicKey, PrivateKey, EncryptedMessage
from typing import Tuple


def generateKey(seed: Seed) -> Tuple[PrivateKey, PublicKey]:
    p, q = seed.p, seed.q
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = randomRelativePrime(phi_n)
    e = inverse_mod(d, phi_n)
    return (PrivateKey(n=n, d=d), PublicKey(n=n, e=e))


def encrypt(publicKey: PublicKey, message: int) -> EncryptedMessage:
    return EncryptedMessage(value=powermod(message, publicKey.e, publicKey.n))


def decrypt(privateKey: PrivateKey, ecrypted_message: EncryptedMessage) -> int:
    return powermod(ecrypted_message.value, privateKey.d, privateKey.n)
