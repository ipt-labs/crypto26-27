import random
from t1 import generate_prime_number
from t23 import GenerateKeyPair
from t45 import Encrypt, Decrypt, Sign, Verify, text_to_int, int_to_text

def to_hex(n):
    res = hex(n)[2:].upper()
    return '0' + res if len(res) % 2 != 0 else res

def from_hex(hex_str):
    clean_str = hex_str.replace(" ", "").replace("\n", "")
    return int(clean_str, 16)

print("[*] Генерація локальних ключів...")
p = generate_prime_number(256)
q = generate_prime_number(256)
local_keys = GenerateKeyPair(p, q)

# Локальні ключі
MY_N = local_keys['public'][0]
MY_E = local_keys['public'][1]
MY_D = local_keys['private'][0]

# Ключі сервера
SERVER_N_HEX = "98DC785CD327753258E17C6AC079A322922C9587535918898982AB37C02149C624A36B8C008BCFEECAE90B895435079AAD7B96780009386701C9566262065BB95A76A1419F40859E75FA484E5AE4BF244FC9BBA3978461BEE4162AE10F82025FF0D96D7E6A9D847558A37005CF829405728012D47AD8AC8E86875EFF51F78D03"
SERVER_E_HEX = "10001"
serv_n = from_hex(SERVER_N_HEX)
serv_e = from_hex(SERVER_E_HEX)

print("\n" + "="*43)
print("ЛОКАЛЬНІ КЛЮЧІ:")
print(f"Modulus (Bytes):\n{to_hex(MY_N)}")
print(f"Public Exponent (Bytes):\n{to_hex(MY_E)}")
print("="*43 + "\n")


print("--- Локально шифруємо -> Сервер розшифровує ---")
msg1 = "TestDecryption"
M1 = text_to_int(msg1)
C1 = Encrypt(M1, serv_e, serv_n)
print(f"Відкритий текст: '{msg1}'")
print(f"Ciphertext (Bytes):\n{to_hex(C1)}\n")

print("--- Сервер шифрує -> Локально розшифровуємо ---")
site_c_hex = input("> Ciphertext з сайту: ")
if site_c_hex:
    C2 = from_hex(site_c_hex)
    M2 = Decrypt(C2, MY_D, MY_N)
    print(f"Розшифрований текст: '{int_to_text(M2)}'\n")


print("--- Локально підписуємо -> Сервер перевіряє ---")
msg3 = "TestVerify"
M3 = text_to_int(msg3)
S3 = Sign(M3, MY_D, MY_N)
print(f"Message (Text): '{msg3}'")
print(f"Signature (Bytes):\n{to_hex(S3)}\n")

print("--- Сервер підписує -> Локально перевіряємо ---")
msg4 = input("> Текст з сайту: ")
site_s_hex = input("> Signature з сайту: ")
if msg4 and site_s_hex:
    M4 = text_to_int(msg4)
    S4 = from_hex(site_s_hex)
    is_valid = Verify(M4, S4, serv_e, serv_n)
    print(f"Результат перевірки підпису сервера: {is_valid}\n")


print("--- Сервер відправляє ключ -> Локально отримуємо ---")
site_key_hex = input("> Key з сайту: ")
site_sig_hex = input("> Signature з сайту: ")

if site_key_hex and site_sig_hex:
    k_enc = from_hex(site_key_hex)
    s_enc = from_hex(site_sig_hex)
    
    k_dec = Decrypt(k_enc, MY_D, MY_N)
    s_dec = Decrypt(s_enc, MY_D, MY_N)
    
    is_auth = Verify(k_dec, s_dec, serv_e, serv_n)
    print(f"Секретний ключ сервера розшифровано:\n{k_dec}")
    print(f"Автентичність сервера: {is_auth}\n")

print("--- Локально відправляємо ключ -> Сервер отримує ---")
k_my = random.randrange(1, 1000000)
s_my = Sign(k_my, MY_D, MY_N)
k_enc_my = Encrypt(k_my, serv_e, serv_n)
s_enc_my = Encrypt(s_my, serv_e, serv_n)

print(f"Key (Bytes):\n{to_hex(k_enc_my)}")
print(f"Signature (Bytes):\n{to_hex(s_enc_my)}")