import json
import random


# Допоміжні функції з п. 1 та п. 3
def modpow(base, exp, mod):
    """Швидке піднесення до степеня за модулем."""
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result


def load_keys(filename):
    """Завантаження ключів із JSON-файлу."""
    with open(filename) as f:
        j = json.load(f)
    n, e, d, p, q = (int(j[k], 16) for k in ("n", "e", "d", "p", "q"))
    return (n, e), (d, p, q)

# ПУНКТ 4. Базові криптографічні операції RSA
def Encrypt(M, public_key):
    """Шифрування повідомлення M відкритим ключем (e, n)."""
    e, n = public_key
    if not (0 <= M < n):
        raise ValueError("Повідомлення M повинно бути в межах 0 <= M < n")
    return modpow(M, e, n)

def Decrypt(C, private_key):
    """Розшифрування криптограми C секретним ключем (d, n)."""
    d, n = private_key
    if not (0 <= C < n):
        raise ValueError("Криптограма C повинна бути в межах 0 <= C < n")
    return modpow(C, d, n)

def Sign(M, private_key):
    """Створення повідомлення з цифровим підписом (M, S) секретним ключем (d, n)."""
    d, n = private_key
    if not (0 <= M < n):
        raise ValueError("Повідомлення M повинно бути в межах 0 <= M < n")
    S = modpow(M, d, n)
    return (M, S)

def Verify(M, S, public_key):
    """Перевірка цифрового підпису S відкритим ключем (e, n)."""
    e, n = public_key
    return modpow(S, e, n) == M


# ПУНКТ 5. Протокол конфіденційного розсилання ключів з підтвердженням справжності
def SendKey(k, sender_private_key, receiver_public_key):
    """
    Процедура відправника (абонент A):
    1. Підписує ключ k своїм секретним ключем (d, n) -> S.
    2. Шифрує k та S відкритим ключем отримувача B (e1, n1) -> (k1, S1).
    """
    _, n = sender_private_key
    if not (0 < k < n):
        raise ValueError("Ключ k повинен задовольняти умову 0 < k < n")

    _, S = Sign(k, sender_private_key)
    k1 = Encrypt(k, receiver_public_key)
    S1 = Encrypt(S, receiver_public_key)
    return S, (k1, S1)


def ReceiveKey(packet, receiver_private_key, sender_public_key):
    """
    Процедура приймаючого (абонент B):
    1. Розшифровує (k1, S1) своїм секретним ключем (d1, n1) -> (k', S').
    2. Перевіряє підпис S' відкритим ключем відправника A (e, n).
    """
    k1, S1 = packet
    k_received = Decrypt(k1, receiver_private_key)
    S_received = Decrypt(S1, receiver_private_key)
    is_authentic = Verify(k_received, S_received, sender_public_key)
    return k_received, S_received, is_authentic


if __name__ == "__main__":
    raw_pub_A, raw_priv_A = load_keys("keys_A.json")
    raw_pub_B, raw_priv_B = load_keys("keys_B.json")

    n, e = raw_pub_A
    d, _, _ = raw_priv_A
    pub_A = (e, n)
    priv_A = (d, n)

    n1, e1 = raw_pub_B
    d1, _, _ = raw_priv_B
    pub_B = (e1, n1)
    priv_B = (d1, n1)

    # --- Перевірка П.4 ---
    print("=== П.4. Шифрування та цифровий підпис RSA ===")
    M = random.randint(2, n - 1)
    print(f"Випадкове відкрите повідомлення M = {M}\n")

    C_A = Encrypt(M, pub_A)
    M_dec_A = Decrypt(C_A, priv_A)
    _, S_A = Sign(M, priv_A)
    valid_A = Verify(M, S_A, pub_A)

    print("--- Абонент A ---")
    print(f"Криптограма C_A      = {C_A}")
    print(f"Розшифроване M_dec_A = {M_dec_A}")
    print(f"Розшифрування вірне? = {'OK' if M_dec_A == M else 'ПОМИЛКА'}")
    print(f"Цифровий підпис S_A  = {S_A}")
    print(f"Підпис дійсний?      = {'OK' if valid_A else 'ПОМИЛКА'}\n")

    C_B = Encrypt(M, pub_B)
    M_dec_B = Decrypt(C_B, priv_B)
    _, S_B = Sign(M, priv_B)
    valid_B = Verify(M, S_B, pub_B)

    print("--- Абонент B ---")
    print(f"Криптограма C_B      = {C_B}")
    print(f"Розшифроване M_dec_B = {M_dec_B}")
    print(f"Розшифрування вірне? = {'OK' if M_dec_B == M else 'ПОМИЛКА'}")
    print(f"Цифровий підпис S_B  = {S_B}")
    print(f"Підпис дійсний?      = {'OK' if valid_B else 'ПОМИЛКА'}\n")

    # --- Перевірка П.5 ---
    print("=== П.5. Протокол розсилання ключів з підтвердженням справжності (A -> B) ===")
    k = random.randint(1, n - 1)

    S, packet = SendKey(k, priv_A, pub_B)
    k1, S1 = packet
    k_recv, S_recv, is_authentic = ReceiveKey(packet, priv_B, pub_A)

    print(f"1. Абонент A вибрав випадковий ключ k   = {k}")
    print(f"2. Абонент A обчислив підпис S          = {S}")
    print(f"3. Передано у відкритий канал k1        = {k1}")
    print(f"   Передано у відкритий канал S1        = {S1}")
    print(f"4. Абонент B розшифрував ключ k'        = {k_recv}")
    print(f"   Абонент B розшифрував підпис S'      = {S_recv}")
    print(f"5. Підпис відправника A підтверджено?   = {'OK' if is_authentic else 'ПОМИЛКА'}")
    print(f"   Отриманий ключ k' збігається з k?    = {'OK' if k == k_recv else 'ПОМИЛКА'}")


# =========================================================================
    # ПЕРЕВІРКА ВЗАЄМОДІЇ З ТЕСТОВИМ СЕРЕДОВИЩЕМ
    # =========================================================================
    def to_hex(num):
        return hex(num)[2:].upper()

    def from_hex(hex_str):
        return int(hex_str.strip(), 16)

    print("\n" + "=" * 60)
    print("ТЕСТУВАННЯ З ВЕБ-СЕРВІСОМ (ЗВОРОТНА ПЕРЕВІРКА)")
    print("=" * 60)

    # --- ПОПЕРЕДНІ ТЕСТИ (Ми -> Сервер) — закоментовано ---
    # srv_n_big_hex = "A3028F59D8F8D7661E48837428C320A8DAE0A54D33C5CBD8C1CA75E0FFB296667873D392C583FA602C46F7EFC7EB2DE82EB660F36BA932D1E56DA6AE672D13B3"
    # srv_e_hex = "10001"
    #
    # if srv_n_big_hex:
    #     pub_srv_big = (from_hex(srv_e_hex), from_hex(srv_n_big_hex))
    #
    #     M_web = random.randint(2, pub_srv_big[1] - 1)
    #     C_web = Encrypt(M_web, pub_srv_big)
    #     print("\n--- Decryption ---")
    #     print(f"Ciphertext : {to_hex(C_web)}")
    #     print(f"Очікуваний Message (звірити):  {to_hex(M_web)}")
    #
    #     M_sign = random.randint(2, n - 1)
    #     _, S_local = Sign(M_sign, priv_A)
    #     print("\n--- Verification ---")
    #     print(f"Message:         {to_hex(M_sign)}")
    #     print(f"Signature:       {to_hex(S_local)}")
    #     print(f"Modulus:         {to_hex(n)}")
    #     print(f"Public exponent: {to_hex(e)}")
    #
    #     k_session = random.randint(1, n - 1)
    #     _, (k1, S1) = SendKey(k_session, priv_A, pub_srv_big)
    #     print("\n--- Receive Key ---")
    #     print(f"Key:                    {to_hex(k1)}")
    #     print(f"Signature:              {to_hex(S1)}")
    #     print(f"Modulus:                {to_hex(n)}")
    #     print(f"Public exponent:        {to_hex(e)}")
    #     print(f"Очікуваний k (звірити): {to_hex(k_session)}")
    #
    # print("\n--- Encryption ---")
    # print(f"Modulus:         {to_hex(n)}")
    # print(f"Public exponent: {to_hex(e)}")
    # C_from_srv_hex = "01E4F45D19FB33521A6894F53A8AC82A5C51E001764319B80E0DCAECCF90C7F76A9994153D69D19053B2B9D16373D0C312EB197DCA7FC6FDAE6BDFB05A2D7C5B"
    # if C_from_srv_hex:
    #     M_dec_web = Decrypt(from_hex(C_from_srv_hex), priv_A)
    #     print(f"Розшифроване локально M: {to_hex(M_dec_web)}")

    # --- ЗВОРОТНА ПЕРЕВІРКА ---
    srv_n_small_hex = "A18CD8362323B0044AB67768FDCA455D5A078BD12CC39348FECCC289043D1E4B"
    srv_e_hex = "10001"
    pub_srv_small = (from_hex(srv_e_hex), from_hex(srv_n_small_hex))

    print("\n--- Дані для вкладки Send Key на сайті (ваш відкритий ключ A) ---")
    print(f"Modulus:         {to_hex(n)}")
    print(f"Public exponent: {to_hex(e)}")

    sig_from_srv_hex = "29FA502FEAE701DF53A4DF2AB7F978BB6B24AC3AA1D7E09410A055E0D921D835"  # Signature із вкладки Signature (ABCDEF12345)
    k1_from_srv_hex = "28A921D3A5B3D19BA7E45CBA16A17A2838B837835260F802036D525D146263AACFD3646437959B260490AD996F0F79765F5D3B235B5FBEFB1173416166B27CF3"   # Зашифрований Key із вкладки Send Key
    s1_from_srv_hex = "410AF9D050804373FA78C24BCD3EEDCDBD2C9D94A19DCF704B1BDF7E6834269B5CB5197F61F8D752F541F014DCC2F863CC018A39E7E32CE79640612E3B1655D9"   # Зашифрована Signature із вкладки Send Key

    if sig_from_srv_hex:
        valid_srv = Verify(from_hex("ABCDEF12345"), from_hex(sig_from_srv_hex), pub_srv_small)
        print(f"\n--- 5.1. Перевірка підпису сервера (Verify) -> {valid_srv} ---")

    if k1_from_srv_hex and s1_from_srv_hex:
        k_recv, _, auth_srv = ReceiveKey(
            (from_hex(k1_from_srv_hex), from_hex(s1_from_srv_hex)),
            priv_A,
            pub_srv_small
        )
        print("\n--- 5.2. Прийом ключа від сервера (ReceiveKey) ---")
        print(f"Розшифрований ключ k (звірити із сайтом): {to_hex(k_recv)}")
        print(f"Справжність відправника підтверджено? -> {auth_srv}")