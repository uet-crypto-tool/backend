from app.core.cryptoSystem import elgamal
from app.core.generators import generateProbablePrime
import secrets


def test_core_cryptoSystem_rsa():
    p = generateProbablePrime(100)
    a = secrets.randbits(100)

    p, a, alpha, beta = elgamal.generateKey(p, a)
    message = secrets.randbits(8)
    encrypted_message = elgamal.encrypt(p, alpha, beta, message)
    decrypted_message = elgamal.decrypt(p, a, encrypted_message)
    assert decrypted_message == message
