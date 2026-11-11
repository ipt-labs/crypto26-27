import json
import random
from task4 import Encrypt, Decrypt, Sign, Verify

def SendKey(k, n, d, n1, e1):
    if n > n1:
        raise ValueError("Для передавання ключа потрібно n <= n1.")
    if not 0 < k < n:
        raise ValueError("Ключ повинен задовольняти умову 0 < k < n.")
    signature = Sign(k, n, d)
    k1 = Encrypt(k, n1, e1)
    s1 = Encrypt(signature, n1, e1)
    return k1, s1

def ReceiveKey(k1, s1, n1, d1, n, e):
    if not (0 <= k1 < n1 and 0 <= s1 < n1):
        raise ValueError("Отримані шифротексти виходять за межі модуля.")
    k = Decrypt(k1, n1, d1)
    signature = Decrypt(s1, n1, d1)
    if not (0 < k < n and 0 <= signature < n):
        raise ValueError("Отриманий ключ або підпис має некоректне значення.")
    if not Verify(k, signature, n, e):
        raise ValueError("Підпис відправника не підтверджено.")
    return k, signature

def main():
    with open("keys.json", encoding="utf-8") as f:
        keys = json.load(f)
    n = keys["A"]["public"]["n"]
    e = keys["A"]["public"]["e"]
    d = keys["A"]["private"]["d"]
    n1 = keys["B"]["public"]["n"]
    e1 = keys["B"]["public"]["e"]
    d1 = keys["B"]["private"]["d"]
    k = random.randrange(1, n)
    k1, s1 = SendKey(k, n, d, n1, e1)
    print("Передавання ключа від абонента A до абонента B")
    print(f"Умова n <= n1: {n <= n1}")
    print("\nАбонент A:")
    print(f"Випадковий ключ k = {k}")
    print(f"Підпис S = k^d mod n = {Sign(k, n, d)}")
    print("\nПередані відкритим каналом значення:")
    print(f"k1 = k^e1 mod n1 = {k1}")
    print(f"S1 = S^e1 mod n1 = {s1}")
    
    received_k, received_s = ReceiveKey(k1, s1, n1, d1, n, e)
    
    print("\nАбонент B:")
    print(f"Відновлений ключ k = k1^d1 mod n1 = {received_k}")
    print(f"Відновлений підпис S = S1^d1 mod n1 = {received_s}")
    print(f"S^e mod n = {pow(received_s, e, n)}")
    print(f"Підпис підтверджено: {Verify(received_k, received_s, n, e)}")
    print(f"Отриманий ключ збігається з початковим: {received_k == k}")
    print("\nКонфіденційність:")
    print("Ключ і підпис зашифровано відкритим ключем B (n1, e1).")
    print("Для розшифрування B використовує свій секретний показник d1.")
    print("\nПідтвердження справжності відправника:")
    print("A створює підпис своїм секретним показником d.")
    print("B перевіряє підпис відкритим ключем A (n, e).")
    
if __name__ == "__main__":
    main()
