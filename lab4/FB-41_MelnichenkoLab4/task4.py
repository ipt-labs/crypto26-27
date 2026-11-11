import json
import random

def Encrypt(message, n, e):
    return pow(message, e, n)
def Decrypt(ciphertext, n, d):
    return pow(ciphertext, d, n)
def Sign(message, n, d):
    return pow(message, d, n)
def Verify(message, signature, n, e):
    return pow(signature, e, n) == message
def main():
    with open("keys.json", encoding="utf-8") as f:
        keys = json.load(f)
    message = random.randrange(
        1, min(keys["A"]["public"]["n"], keys["B"]["public"]["n"])
    )
    print(f"Відкрите повідомлення M = {message}")
    for name in ("A", "B"):
        n = keys[name]["public"]["n"]
        e = keys[name]["public"]["e"]
        d = keys[name]["private"]["d"]
        ciphertext = Encrypt(message, n, e)
        decrypted = Decrypt(ciphertext, n, d)
        signature = Sign(message, n, d)
        verified = Verify(message, signature, n, e)
        print(f"\nАбонент {name}:")
        print(f"Шифротекст C = {ciphertext}")
        print(f"Розшифроване повідомлення M' = {decrypted}")
        print(f"M' = M: {decrypted == message}")
        print(f"Цифровий підпис S = {signature}")
        print(f"Підписане повідомлення (M, S) = ({message}, {signature})")
        print(f"Результат перевірки підпису: {verified}")
        
if __name__ == "__main__":
    main()
