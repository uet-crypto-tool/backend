from app.core.utils import mul_mod, inverse_mod


def encrypt(a: int, b: int, message: str) -> str:
    """
    Encrypts a message using the Affine Cipher.

    Args:
        a (int): The multiplier used in the encryption function, must be coprime with 26.
        b (int): The shift value added during encryption.
        message (str): The plaintext message to be encrypted.

    Returns:
        str: The encrypted message.

    The function encrypts the message using the Affine Cipher formula:
        E(x) = (a * x + b) % 26
    Where `x` is the index of the character in the alphabet.
    Non-alphabetic characters (spaces, punctuation, etc.) are not altered.
    """
    result = ""
    for char in message:
        if char.isalpha():
            start = (
                ord("A") if char.isupper() else ord("a")
            )  # Determine case (uppercase or lowercase)
            result += chr(
                start + (mul_mod(a, ord(char) - start, 26) + b) % 26
            )  # Apply the Affine Cipher formula
        else:
            result += char  # Non-alphabet characters are unchanged

    return result


def decrypt(a: int, b: int, message: str) -> str:
    """
    Decrypts a message that was encrypted using the Affine Cipher.

    Args:
        a (int): The multiplier used in the encryption function, must be coprime with 26.
        b (int): The shift value added during encryption.
        message (str): The encrypted message to be decrypted.

    Returns:
        str: The decrypted message.

    The function decrypts the message using the Affine Cipher inverse formula:
        D(x) = a^-1 * (x - b) % 26
    Where `a^-1` is the modular inverse of `a` modulo 26, and `x` is the index of the character in the alphabet.
    Non-alphabetic characters (spaces, punctuation, etc.) are not altered.
    """
    result = ""
    for char in message:
        if char.isalpha():
            start = (
                ord("A") if char.isupper() else ord("a")
            )  # Determine case (uppercase or lowercase)
            result += chr(
                (
                    start + mul_mod(inverse_mod(a, 26), ord(char) - start - b, 26) % 26
                )  # Apply the inverse Affine Cipher formula
            )
        else:
            result += char  # Non-alphabet characters are unchanged

    return result
