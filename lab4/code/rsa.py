from gen_RSA_pair import *
import random
import re


def int_to_hex(val):
    if val == 0:
        return "00"
    length = (val.bit_length() + 7) // 8
    return val.to_bytes(length, 'big').hex()


def hex_to_int(hex_str):
    s = "".join(hex_str.split())
    if s[:2] in ("0x", "0X"):
        s = s[2:]
    if not re.fullmatch(r"[0-9a-fA-F]+", s):
        raise ValueError(f"Некоректний hex-рядок: {hex_str!r}")
    return int(s, 16)


def generate_random_hex_message(num_bytes = 32):
    first_byte = bytes([random.randint(1, 255)])
    rest_bytes = random.randbytes(num_bytes - 1)
    return (first_byte + rest_bytes).hex()


def Encrypt(plain_text_hex, public_key):
    n, e = public_key
    m = hex_to_int(plain_text_hex)
    if not (0 <= m < n):
        raise ValueError("Повідомлення M має задовольняти умову 0 <= M < n.")
    
    c = pow(m, e, n)
    return int_to_hex(c)


def Decrypt(cipher_text_hex, private_key):
    d, p, q = private_key
    n = p * q
    c = hex_to_int(cipher_text_hex)
    if not (0 <= c < n):
        raise ValueError("Криптограма C має задовольняти умову 0 <= C < n.")
    
    m = pow(c, d, n)
    return int_to_hex(m)


def Sign(message_hex, private_key):
    d, p, q = private_key
    n = p * q
    m = hex_to_int(message_hex)
    if not (0 <= m < n):
        raise ValueError("Повідомлення M має задовольняти умову 0 <= M < n.")
    
    s = pow(m, d, n)
    signature_hex = int_to_hex(s)
    return message_hex, signature_hex


def Verify(signed_message, public_key):
    n, e = public_key
    msg_hex, sig_hex = signed_message
    
    m = hex_to_int(msg_hex)
    s = hex_to_int(sig_hex)
    if not (0 <= s < n):
        return False
    
    recovered_m = pow(s, e, n)
    return m == recovered_m


if __name__ == "__main__":
    keys = GetKeyPairs()

    for key_pair in keys:
        print("\n" + "-" * 50)
        print(f"Приватний ключ (d, p, q) (hex): ({int_to_hex(key_pair[0][0])}, {int_to_hex(key_pair[0][1])}, {int_to_hex(key_pair[0][2])})")
        print(f"Публічний ключ (n, e) (hex): ({int_to_hex(key_pair[1][0])}, {int_to_hex(key_pair[1][1])})")
        print("\n")
        
        message_hex = generate_random_hex_message(32)
        print("Оригінальне повідомлення (hex):", message_hex)

        encrypted_message = Encrypt(message_hex, key_pair[1])
        print("Шифротекст (hex):", encrypted_message)

        decrypted_message = Decrypt(encrypted_message, key_pair[0])
        print("Розшифроване повідомлення (hex):", decrypted_message)

        signed_message = Sign(message_hex, key_pair[0])
        print("Підпис (hex):", signed_message[1])

        is_verified = Verify(signed_message, key_pair[1])
        print("Перевірка підпису:  ", is_verified)
