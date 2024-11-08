from app.core.utils import mul_mod, inverse_mod


def encrypt(a: int, b: int, message: str) -> str:
    result = ""
    for char in message:
        if char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            result += chr(start + (mul_mod(a, ord(char) - start, 26) + b) % 26)
        else:
            result += char

    return result


def decrypt(a: int, b: int, message: str) -> str:
    result = ""
    for char in message:
        if char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            result += chr(
                (start + mul_mod(inverse_mod(a, 26), ord(char) - start - b, 26) % 26) 
            )
        else:
            result += char

    return result
