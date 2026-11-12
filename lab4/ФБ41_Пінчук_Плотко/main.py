import secrets
import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 1. МАТЕМАТИЧНА БАЗА (Ітеративний Евклід та схема Горнера)
# ============================================================

def gcd(a: int, b: int) -> int:
    """Найбільший спільний дільник (алгоритм Евкліда)."""
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a: int, b: int):
    """Розширений алгоритм Евкліда: повертає (d, u, v), де a*u + b*v = d."""
    r0, r1 = a, b
    u0, u1 = 1, 0
    v0, v1 = 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return r0, u0, v0

def mod_inverse(a: int, m: int) -> int:
    """Обернений елемент a^(-1) mod m."""
    d, u, _ = extended_gcd(a % m, m)
    if d != 1:
        raise ValueError("Обернений елемент не існує")
    return u % m

def mod_pow(base: int, exp: int, mod: int) -> int:
    """Швидке піднесення до степеня за модулем (схема Горнера)."""
    res = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            res = (res * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return res

# ============================================================
# 2. ТЕСТИ НА ПРОСТОТУ ТА ГЕНЕРАЦІЯ ПРОСТИХ ЧИСЕЛ (Пункти 1-2)
# ============================================================

SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97
]

def trial_division(n: int):
    """Попередній тест пробних ділень на малі прості числа."""
    if n < 2:
        return False, None
    for p in SMALL_PRIMES:
        if n == p:
            return True, None
        if n % p == 0:
            return False, p
    return True, None

def miller_rabin(p: int, k: int = 20):
    """
    Імовірнісний тест Міллера-Рабіна.
    Повертає (is_prime, trace_first_base) для звіту.
    """
    if p < 2:
        return False, {}
    if p in SMALL_PRIMES:
        return True, {}
    if p % 2 == 0:
        return False, {}

    # Крок 0: Розклад p - 1 = d * 2^s
    d = p - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    trace = {}
    for i in range(k):
        x_base = secrets.randbelow(p - 3) + 2
        g = gcd(x_base, p)
        if g > 1:
            if i == 0:
                trace = {"base": x_base, "d": d, "s": s, "gcd": g, "result": "Складене (gcd > 1)"}
            return False, trace

        # Крок 2.1: x_0 = x^d mod p
        x = mod_pow(x_base, d, p)
        seq = [x]

        if x == 1 or x == p - 1:
            passed = True
        else:
            passed = False
            # Крок 2.2: послідовне піднесення до квадрату для r від 1 до s-1
            for _ in range(1, s):
                x = (x * x) % p
                seq.append(x)
                if x == p - 1:
                    passed = True
                    break
                if x == 1:
                    passed = False
                    break

        if i == 0:
            trace = {
                "base": x_base,
                "d": d,
                "s": s,
                "sequence": seq,
                "result": "Сильно псевдопросте" if passed else "Складене"
            }

        if not passed:
            return False, trace

    return True, trace

def generate_prime(bits: int = 256):
    """Генерація випадкового простого числа заданої бітової довжини."""
    rejected = []
    while True:
        # Генеруємо непарне число рівно на `bits` біт (старший і молодший біти = 1)
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1

        ok_trial, divisor = trial_division(candidate)
        if not ok_trial:
            rejected.append((candidate, f"Тест пробних ділень (ділиться на {divisor})"))
            continue

        ok_mr, trace = miller_rabin(candidate, k=20)
        if ok_mr:
            return candidate, rejected, trace
        else:
            rejected.append((candidate, "Не пройшло тест Міллера-Рабіна"))

# ============================================================
# 3. СІМ ОБОВ'ЯЗКОВИХ ПРОЦЕДУР RSA (Пункти 3-5)
# ============================================================

def GenerateKeyPair(bits: int = 256):
    """1. Генерація ключової пари RSA: відкритий (e, n) та секретний (d, p, q)."""
    p, rej_p, trace_p = generate_prime(bits)
    q, rej_q, trace_q = generate_prime(bits)
    while p == q:
        q, extra_rej, trace_q = generate_prime(bits)
        rej_q.extend(extra_rej)

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    while gcd(e, phi) != 1:
        e += 2

    d = mod_inverse(e, phi)
    public_key = (e, n)
    private_key = (d, p, q)
    meta = {
        "p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d,
        "rejected_p": rej_p, "rejected_q": rej_q,
        "trace_p": trace_p, "trace_q": trace_q
    }
    return public_key, private_key, meta

def Encrypt(M: int, public_key: tuple) -> int:
    """2. Шифрування повідомлення M відкритим ключем адресата (e, n)."""
    e, n = public_key
    if not (0 <= M < n):
        raise ValueError("Повідомлення M має бути в межах [0, n-1]")
    return mod_pow(M, e, n)

def Decrypt(C: int, private_key: tuple) -> int:
    """3. Розшифрування криптограми C секретним ключем (d, p, q)."""
    d, p, q = private_key
    n = p * q
    if not (0 <= C < n):
        raise ValueError("Криптограма C має бути в межах [0, n-1]")
    return mod_pow(C, d, n)

def Sign(M: int, private_key: tuple) -> int:
    """4. Створення цифрового підпису: S = M^d mod n."""
    d, p, q = private_key
    n = p * q
    if not (0 <= M < n):
        raise ValueError("Повідомлення M має бути в межах [0, n-1]")
    return mod_pow(M, d, n)

def Verify(M: int, S: int, public_key: tuple) -> bool:
    """5. Перевірка цифрового підпису: чи виконується M == S^e mod n."""
    e, n = public_key
    if not (0 <= S < n):
        return False
    return M == mod_pow(S, e, n)

def SendKey(k: int, private_key_A: tuple, public_key_B: tuple) -> tuple:
    """
    6. Відправлення секретного ключа k від А до В:
    Підпис: S = k^d mod n
    Шифрування: k1 = k^e1 mod n1, S1 = S^e1 mod n1
    """
    d, p, q = private_key_A
    e1, n1 = public_key_B
    n = p * q
    if not (0 < k < n):
        raise ValueError("Ключ k має бути в межах 0 < k < n")
    if n1 < n:
        raise ValueError("Порушено умову протоколу: має бути n1 >= n")

    S = mod_pow(k, d, n)
    k1 = mod_pow(k, e1, n1)
    S1 = mod_pow(S, e1, n1)
    return k1, S1

def ReceiveKey(packet: tuple, private_key_B: tuple, public_key_A: tuple) -> tuple:
    """
    7. Отримання та перевірка ключа k абонентом В:
    Конфіденційність: k = k1^d1 mod n1, S = S1^d1 mod n1
    Автентифікація: перевірка k == S^e mod n
    """
    k1, S1 = packet
    d1, p1, q1 = private_key_B
    e, n = public_key_A
    n1 = p1 * q1

    k = mod_pow(k1, d1, n1)
    S = mod_pow(S1, d1, n1)
    is_authentic = (k == mod_pow(S, e, n)) and (0 < k < n)
    return k, S, is_authentic

# ============================================================
# 4. ЗАПУСК ЕКСПЕРИМЕНТУ ТА АВТОЗБЕРЕЖЕННЯ У ФАЙЛИ
# ============================================================

def to_hex(val: int) -> str:
    return hex(val)[2:].upper()

def main():
    report = []
    def log(text=""):
        print(text)
        report.append(str(text))

    log("=" * 70)
    log("КОМП'ЮТЕРНИЙ ПРАКТИКУМ №4 — КРИПТОСИСТЕМА RSA ТА ЦИФРОВИЙ ПІДПИС")
    log("=" * 70)

    # 1. Генерація пар ключів з виконанням умови pq <= p1*q1 (n <= n1)
    pub_A, priv_A, meta_A = GenerateKeyPair(256)
    pub_B, priv_B, meta_B = GenerateKeyPair(256)
    if pub_A[1] > pub_B[1]:
        pub_A, pub_B = pub_B, pub_A
        priv_A, priv_B = priv_B, priv_A
        meta_A, meta_B = meta_B, meta_A

    e, n = pub_A
    d, p, q = priv_A
    e1, n1 = pub_B
    d1, p1, q1 = priv_B

    # 2. Вивід параметрів та проміжних результатів Міллера-Рабіна
    for label, meta in [("А", meta_A), ("B", meta_B)]:
        log(f"\n--- ПАРАМЕТРИ АБОНЕНТА {label} ---")
        log(f"p ({meta['p'].bit_length()} біт) = {meta['p']}")
        log(f"q ({meta['q'].bit_length()} біт) = {meta['q']}")
        log(f"n ({meta['n'].bit_length()} біт) = {meta['n']}")
        log(f"phi(n) = {meta['phi']}")
        log(f"e = {meta['e']}")
        log(f"d = {meta['d']}")
        log(f"Відхилено кандидатів при пошуку p: {len(meta['rejected_p'])}, при пошуку q: {len(meta['rejected_q'])}")

    tr = meta_A["trace_p"]
    log("\n--- ДОПОВНЕННЯ ДО П.1: Проміжні результати Міллера-Рабіна (для простого p абонента А) ---")
    log(f"Досліджуване просте число p = {p}")
    log(f"Розклад p - 1 = d * 2^s: d = {tr['d']}, s = {tr['s']}")
    log(f"Випадкова основа x = {tr['base']}")
    log(f"gcd(x, p) = 1")
    for idx, val in enumerate(tr["sequence"]):
        log(f"  Крок r={idx}: x^({tr['d']} * 2^{idx}) mod p = {val}")
    log(f"Висновок для основи: {tr['result']}")

    # 3. Перевірка математичних співвідношень RSA (Пункт 3)
    log("\n--- П.3: ПЕРЕВІРКА СПІВВІДНОШЕНЬ КОРЕКТНОСТІ RSA ---")
    checks = [
        ("p != q та p1 != q1", p != q and p1 != q1),
        ("n == p * q", n == p * q),
        ("n1 == p1 * q1", n1 == p1 * q1),
        ("Умова протоколу n <= n1 (pq <= p1*q1)", n <= n1),
        ("gcd(e, phi(n)) == 1", gcd(e, meta_A["phi"]) == 1),
        ("(e * d) mod phi(n) == 1", (e * d) % meta_A["phi"] == 1),
        ("gcd(e1, phi(n1)) == 1", gcd(e1, meta_B["phi"]) == 1),
        ("(e1 * d1) mod phi(n1) == 1", (e1 * d1) % meta_B["phi"] == 1),
    ]
    for name, ok in checks:
        log(f"  [{'OK' if ok else 'FAIL'}] {name}")

    # 4. Шифрування, розшифрування та цифровий підпис для А і В (Пункт 4)
    log("\n--- П.4: ШИФРУВАННЯ, РОЗШИФРУВАННЯ ТА ЦИФРОВИЙ ПІДПИС ---")
    M_A = secrets.randbelow(n - 2) + 1
    C_AtoB = Encrypt(M_A, pub_B)
    M_A_dec = Decrypt(C_AtoB, priv_B)
    S_A = Sign(M_A, priv_A)
    ver_A = Verify(M_A, S_A, pub_A)

    log("[Напрямок А -> B та підпис абонента А]")
    log(f"  Відкрите повідомлення M_A = {M_A}")
    log(f"  Криптограма C (зашифровано для B) = {C_AtoB}")
    log(f"  Розшифровано абонентом B = {M_A_dec} (Збігається: {M_A == M_A_dec})")
    log(f"  Цифровий підпис абонента А (S_A) = {S_A}")
    log(f"  Перевірка підпису Verify(M_A, S_A, pub_A) = {ver_A}")

    M_B = secrets.randbelow(n - 2) + 1
    C_BtoA = Encrypt(M_B, pub_A)
    M_B_dec = Decrypt(C_BtoA, priv_A)
    S_B = Sign(M_B, priv_B)
    ver_B = Verify(M_B, S_B, pub_B)

    log("\n[Напрямок B -> А та підпис абонента B]")
    log(f"  Відкрите повідомлення M_B = {M_B}")
    log(f"  Криптограма C (зашифровано для А) = {C_BtoA}")
    log(f"  Розшифровано абонентом А = {M_B_dec} (Збігається: {M_B == M_B_dec})")
    log(f"  Цифровий підпис абонента B (S_B) = {S_B}")
    log(f"  Перевірка підпису Verify(M_B, S_B, pub_B) = {ver_B}")

    # 5. Протокол конфіденційного розсилання ключів (Пункт 5)
    log("\n--- П.5: ПРОТОКОЛ КОНФІДЕНЦІЙНОГО РОЗСИЛАННЯ КЛЮЧІВ (А -> B) ---")
    k_secret = secrets.randbelow(n - 2) + 1
    k1, S1 = SendKey(k_secret, priv_A, pub_B)
    k_rec, S_rec, auth_ok = ReceiveKey((k1, S1), priv_B, pub_A)

    log(f"1. Абонент А обирає секретний ключ k (0 < k < n): k = {k_secret}")
    log(f"2. Абонент А обчислює підпис S = k^d mod n (забезпечує АВТЕНТИФІКАЦІЮ секретним ключем d_A): S = {S_rec}")
    log(f"3. Абонент А шифрує (k, S) відкритим ключем B (e1, n1) (забезпечує КОНФІДЕНЦІЙНІСТЬ):")
    log(f"   Відправлено у відкритий канал пакет: k1 = {k1}, S1 = {S1}")
    log(f"4. Абонент В розшифровує пакет власним секретним ключем d1 (модуль n1):")
    log(f"   Отримано k = {k_rec}, отримано S = {S_rec}")
    log(f"5. Абонент В перевіряє підпис відкритим ключем А (e, n): k == S^e mod n -> {auth_ok}")
    log(f"   Підсумок протоколу: ключ успішно та автентично передано = {k_secret == k_rec and auth_ok}")

    # --- ЗБЕРЕЖЕННЯ ФАЙЛІВ ---
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")

    with open("candidates.txt", "w", encoding="utf-8") as f:
        f.write("=== ВІДХИЛЕНІ КАНДИДАТИ У ПРОСТІ ЧИСЛА ===\n")
        for label, meta in [("Абонент А", meta_A), ("Абонент B", meta_B)]:
            f.write(f"\n--- {label}: пошук p (всього відхилено {len(meta['rejected_p'])}) ---\n")
            for num, reason in meta["rejected_p"]:
                f.write(f"{num} — {reason}\n")
            f.write(f"\n--- {label}: пошук q (всього відхилено {len(meta['rejected_q'])}) ---\n")
            for num, reason in meta["rejected_q"]:
                f.write(f"{num} — {reason}\n")

    with open("keys.json", "w", encoding="utf-8") as f:
        json.dump({
            "Abonent_A": {"e": e, "n": n, "d": d, "p": p, "q": q},
            "Abonent_B": {"e1": e1, "n1": n1, "d1": d1, "p1": p1, "q1": q1}
        }, f, indent=4)

    with open("server_hex.txt", "w", encoding="utf-8") as f:
        f.write("=== ДАНІ У ФОРМАТІ HEX ДЛЯ САЙТУ asymcryptwebservice.appspot.com ===\n\n")
        f.write(f"[Абонент А — для вставлення у поля Modulus та Exponents на сайті]\n")
        f.write(f"Modulus (n_A HEX): {to_hex(n)}\n")
        f.write(f"Public exp (e_A HEX): {to_hex(e)}\n")
        f.write(f"Private exp (d_A HEX): {to_hex(d)}\n\n")
        f.write(f"[Тест шифрування/підпису Абонента А у HEX]\n")
        f.write(f"Message (M_A HEX): {to_hex(M_A)}\n")
        f.write(f"Ciphertext (C_BtoA на ключі А, де M=M_B): Message={to_hex(M_B)} -> Ciphertext={to_hex(C_BtoA)}\n")
        f.write(f"Signature (S_A HEX для M_A): {to_hex(S_A)}\n\n")
        f.write(f"[Абонент B — для перевірки SendKey/Encrypt]\n")
        f.write(f"Modulus (n_B HEX): {to_hex(n1)}\n")
        f.write(f"Public exp (e_B HEX): {to_hex(e1)}\n")
        f.write(f"Private exp (d_B HEX): {to_hex(d1)}\n")
        f.write(f"Ciphertext (C_AtoB на ключі B для M_A): {to_hex(C_AtoB)}\n")

    print("\n[+] Згенеровано файли: results.txt, candidates.txt, keys.json, server_hex.txt")

if __name__ == "__main__":
    main()