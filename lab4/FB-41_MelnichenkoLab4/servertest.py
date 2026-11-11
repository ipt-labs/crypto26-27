from task4 import Encrypt

n = int(
    "CA979AE63058E844CB08540251CBBF44478094584B0DF8E6A7A6CC2EE5D93C44"
    "B77BAB94DEA2B4D47FC1F4C5584A6ABE65E3BA171A58F347443B44B64B168E45",
    16
)
e = int("10001", 16)
message = 123456789
ciphertext = Encrypt(message, n, e)
print(f"Повідомлення DEC: {message}")
print(f"Повідомлення HEX: {message:X}")
print(f"Шифротекст HEX: {ciphertext:X}")
