from app.core.cryptoSystem import affine
from app.core.utils import randomRelativePrime
import secrets

def test_pipeline():
    message = "HelloWorld"
    a = randomRelativePrime(26)
    b = secrets.randbits(100)
    encrypted_message = affine.encrypt(a, b, message)
    decrypted_message = affine.decrypt(a, b, encrypted_message)
    assert decrypted_message == message
