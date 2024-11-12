def encrypt(shift: int, message: str) -> str:
    """
    Encrypts a message using Caesar Cipher encryption.

    Args:
        shift (int): The number of positions to shift each letter in the message.
        message (str): The plaintext message to be encrypted.

    Returns:
        str: The encrypted message.

    The function shifts each letter in the message by the specified number of positions.
    Non-alphabetic characters (spaces, punctuation, etc.) are left unchanged.
    The shift is wrapped around if it exceeds the length of the alphabet (26 letters).
    """
    shift = shift % 26  # Ensure the shift is within the range of 0-25

    result = ""
    for char in message:
        if char.isalpha():
            start = (
                ord("A") if char.isupper() else ord("a")
            )  # Determine case (uppercase or lowercase)
            result += chr(
                start + (ord(char) - start + shift) % 26
            )  # Shift and wrap around if necessary
        else:
            result += char  # Non-alphabet characters are unchanged

    return result


def decrypt(shift: int, message: str) -> str:
    """
    Decrypts a message that was encrypted using Caesar Cipher encryption.

    Args:
        shift (int): The number of positions the message was shifted during encryption.
        message (str): The encrypted message to be decrypted.

    Returns:
        str: The decrypted message.

    The function shifts each letter in the message by the specified number of positions in reverse.
    Non-alphabetic characters (spaces, punctuation, etc.) are left unchanged.
    The shift is wrapped around if it exceeds the length of the alphabet (26 letters).
    """
    shift = shift % 26  # Ensure the shift is within the range of 0-25

    result = ""
    for char in message:
        if char.isalpha():
            start = (
                ord("A") if char.isupper() else ord("a")
            )  # Determine case (uppercase or lowercase)
            result += chr(
                start + (ord(char) - start - shift) % 26
            )  # Reverse shift and wrap around if necessary
        else:
            result += char  # Non-alphabet characters are unchanged

    return result
