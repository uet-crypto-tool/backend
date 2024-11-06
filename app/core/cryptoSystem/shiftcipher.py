def encrypt(shift: int, message: str) -> str:
    shift = shift % 26

    result = ""
    for char in message:
        if char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            result += chr(start + (ord(char) - start + shift) % 26)
        else:
            result += char

    return result


def decrypt(shift: int, message: str) -> str:
    shift = shift % 26

    result = ""
    for char in message:
        if char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            result += chr(start + (ord(char) - start - shift) % 26)
        else:
            result += char

    return result
