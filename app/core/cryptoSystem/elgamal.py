from app.core.utils import powermod, mul_mod, randomRelativePrime
from app.core.generators import randomIntInRange
from app.schemas.elgamal_schemas import Seed, PublicKey, PrivateKey, EncryptedMessage
from typing import Tuple


def generateKey(seed: Seed) -> Tuple[PrivateKey, PublicKey]:
    alpha = randomRelativePrime(seed.p)
    beta = powermod(alpha, seed.a, seed.p)
    return (
        PrivateKey(p=seed.p, a=seed.a, alpha=alpha),
        PublicKey(p=seed.p, alpha=alpha, beta=beta),
    )


def encrypt(publicKey: PublicKey, message: int) -> EncryptedMessage:
    k = randomIntInRange(1, publicKey.p - 1)
    y1 = powermod(publicKey.alpha, k, publicKey.p)
    y2 = mul_mod(message, powermod(publicKey.beta, k, publicKey.p), publicKey.p)
    return EncryptedMessage(y1=y1, y2=y2)


def decrypt(privateKey: PrivateKey, encrypted_message: EncryptedMessage) -> int:
    y1, y2 = encrypted_message.y1, encrypted_message.y2
    return mul_mod(y2, powermod(y1, -privateKey.a, privateKey.p), privateKey.p)
