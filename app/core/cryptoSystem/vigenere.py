def encrypt(key: str, message: str) -> str:
    result = ""
    for i in range(len(message)):
        char = message[i]
        charKey = key[i % len(key)]
        if char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            index_char = ord(char) - start
            index_key = ord(charKey) - start
            result += chr(start + (index_char + index_key) % 26)
        else:
            result += char

    return result


def decrypt(key: str, message: str) -> str:
    result = ""
    for i in range(len(message)):
        char = message[i]
        charKey = key[i % len(key)]
        if char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            index_char = ord(char) - start
            index_key = ord(charKey) - start
            result += chr(start + (index_char - index_key) % 26)
        else:
            result += char

    return result
