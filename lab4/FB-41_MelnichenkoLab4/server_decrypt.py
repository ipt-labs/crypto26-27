import json
from task4 import Decrypt

with open("keys.json", encoding="utf-8") as f:
    keys = json.load(f)
ciphertext = int(input("Шифротекст сервера HEX: ").strip(), 16)
n = keys["A"]["public"]["n"]
d = keys["A"]["private"]["d"]
message = Decrypt(ciphertext, n, d)
print(f"Розшифроване повідомлення DEC: {message}")
print(f"Розшифроване повідомлення HEX: {message:X}")
print(f"Збіг із початковим повідомленням: {message == 123456789}")
