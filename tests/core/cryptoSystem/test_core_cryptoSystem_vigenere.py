from app.core.cryptoSystem import vigenere


def test_pipeline():
    message = "HelloWorld"
    key = "key"
    encrypted_message = vigenere.encrypt(key, message)
    decrypted_message = vigenere.decrypt(key, encrypted_message)
    assert decrypted_message == message
