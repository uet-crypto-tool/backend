from app.core.cryptoSystem import shiftcipher
import secrets


def test_pipeline():
    message = "HelloWorld"
    shift = secrets.randbits(100)
    encrypted_message = shiftcipher.encrypt(shift, message)
    decrypted_message = shiftcipher.decrypt(shift, encrypted_message)
    assert decrypted_message == message
