def encrypt(key: str, message: str) -> str:
    """
    Encrypts a message using the Vigenère cipher.

    Args:
        key (str): The key used for encryption. It is repeated to match the length of the message.
        message (str): The plaintext message to be encrypted.

    Returns:
        str: The encrypted message.

    The function encrypts the message by shifting each letter according to the corresponding letter in the key.
    Non-alphabetic characters (spaces, punctuation, etc.) are not altered.
    The key is repeated as necessary to match the length of the message.
    """
    result = ""
    for i in range(len(message)):
        char = message[i]
        charKey = key[i % len(key)]  # Repeat key to match message length
        if char.isalpha():
            start = (
                ord("A") if char.isupper() else ord("a")
            )  # Determine case (uppercase or lowercase)
            index_char = ord(char) - start
            index_key = ord(charKey) - start
            result += chr(
                start + (index_char + index_key) % 26
            )  # Shift character by key's corresponding letter
        else:
            result += char  # Non-alphabet characters are unchanged

    return result


def decrypt(key: str, message: str) -> str:
    """
    Decrypts a message that was encrypted using the Vigenère cipher.

    Args:
        key (str): The key used for decryption. It is repeated to match the length of the encrypted message.
        message (str): The encrypted message to be decrypted.

    Returns:
        str: The decrypted message.

    The function decrypts the message by shifting each letter in the reverse direction according to the key.
    Non-alphabetic characters (spaces, punctuation, etc.) are not altered.
    The key is repeated as necessary to match the length of the encrypted message.
    """
    result = ""
    for i in range(len(message)):
        char = message[i]
        charKey = key[i % len(key)]  # Repeat key to match message length
        if char.isalpha():
            start = (
                ord("A") if char.isupper() else ord("a")
            )  # Determine case (uppercase or lowercase)
            index_char = ord(char) - start
            index_key = ord(charKey) - start
            result += chr(
                start + (index_char - index_key) % 26
            )  # Reverse shift for decryption
        else:
            result += char  # Non-alphabet characters are unchanged

    return result
