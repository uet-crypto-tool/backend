from app.core.cryptoSystem.asymmetric import rsa
from app.core.prime.generator import generateProbablePrime
import secrets


def test_core_cryptoSystem_rsa():
    p = generateProbablePrime(100)
    q = generateProbablePrime(100)

    n, d, e = rsa.generateKey(p, q)
    message = secrets.randbits(8)
    encrypted_message = rsa.encrypt(n, e, message)
    decrypted_message = rsa.decrypt(n, d, encrypted_message)
    assert decrypted_message == message
