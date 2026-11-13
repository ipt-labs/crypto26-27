import random
import json
import os
import sys
KEYS_FILE = "rsa_keys.json"

def generate_small_primes(limit=1000):
    sieve = [True] * (limit + 1)
    primes = []
    for p in range(2, limit + 1):
        if sieve[p]:
            primes.append(p)
            for i in range(p * p, limit + 1, p):
                sieve[i] = False
    return primes

SMALL_PRIMES = generate_small_primes(1000)

def trial_division(n):
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if p * p > n:
            break
        if n % p == 0:
            return n == p
    return True

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def miller_rabin(p, k=20, debug=False):
    if p < 2: return False
    if p in (2, 3): return True
    if p % 2 == 0: return False
    s = 0
    d = p - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    used_bases = set()
    k = min(k, p - 3)
    for i in range(k):
        x = random.randint(2, p - 2)
        while x in used_bases:
            x = random.randint(2, p - 2)
        used_bases.add(x)
        if gcd(x, p) > 1:
            return False
        show_debug = debug and (i == 0)
        if show_debug:
            print(f"\n--- Доповнення до п.1: Проміжні результати Міллера-Рабіна ---")
            print(f"Тестуємо просте число p = {p}")
            print(f"Крок 0: Розклад p-1: s = {s}, d = {d}")
            print(f"Крок 1: Обрана основа x = {x}")
        x_r = pow(x, d, p)
        if show_debug:
            print(f"Крок 2.1: x^d mod p = {x_r}")
        if x_r == 1 or x_r == p - 1:
            if show_debug: print("-> Число сильно псевдопросте за цією основою (умова 2.1).")
            continue
        is_pseudoprime = False
        for r in range(1, s):
            x_r = pow(x_r, 2, p)
            if show_debug:
                print(f"Крок 2.2 (r={r}): x_r = x_r^2 mod p = {x_r}")
            if x_r == p - 1:
                is_pseudoprime = True
                if show_debug: print("-> Число сильно псевдопросте (знайдено p-1).")
                break
            elif x_r == 1:
                if show_debug: print("-> Знайдено 1, перевірка провалена.")
                break
        if not is_pseudoprime:
            return False
    return True


def generate_large_prime(bits=256, verbose=False):
    rejected_trial = 0
    rejected_mr = 0
    total_checked = 0
    while True:
        n0 = random.getrandbits(bits)
        n0 |= (1 << (bits - 1)) | 1
        limit = (1 << bits) - 1
        i = 0
        while True:
            candidate = n0 + 2 * i
            if candidate > limit:
                break
            total_checked += 1
            if not trial_division(candidate):
                rejected_trial += 1
                i += 1
                continue
            if miller_rabin(candidate, k=20):
                if verbose:
                    print(f"\n[Статистика генерації]")
                    print(f"Всього перевірено кандидатів: {total_checked}")
                    print(f"Відхилено пробними діленнями: {rejected_trial}")
                    print(f"Відхилено тестом Міллера-Рабіна: {rejected_mr}")
                return candidate
            rejected_mr += 1
            i += 1


def ext_gcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def mod_inverse(a, m):
    g, x, _ = ext_gcd(a, m)
    if g != 1:
        raise ValueError("Оберненого елемента не існує (gcd != 1)")
    return x % m

def mod_pow(x, power, m):
    y = 1
    x %= m
    for bit in bin(power)[2:]:
        y = (y * y) % m
        if bit == "1":
            y = (y * x) % m
    return y

def GenerateKeyPair(p, q, e=2 ** 16 + 1):
    n = p * q
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        while True:
            e = random.randrange(2, phi - 1)
            if gcd(e, phi) == 1:
                break
    d = mod_inverse(e, phi)
    return (n, e), (d, p, q)


def check_key_pair(public, private, verbose=True):
    n, e = public
    d, p, q = private
    phi = (p - 1) * (q - 1)
    M = random.randrange(2, n - 1)
    checks = {
        "n = p*q": n == p * q,
        "phi(n) = (p-1)(q-1)": phi == n - p - q + 1,
        "2 <= e <= phi-1": 2 <= e <= phi - 1,
        "gcd(e, phi) = 1": gcd(e, phi) == 1,
        "e*d = 1 (mod phi)": (e * d) % phi == 1,
        "(M^e)^d = M (mod n) для випадкового M": mod_pow(mod_pow(M, e, n), d, n) == M,
    }
    if verbose:
        print(f"  p   = {p}\n  q   = {q}\n  n   = {n}\n  phi = {phi}")
        print(f"  e   = {e}\n  d   = {d}")
        for name, ok in checks.items():
            print(f"  [{'OK' if ok else 'FAIL'}] {name}")
    return all(checks.values())


def build_keys(bits=256):
    p, q = generate_large_prime(bits), generate_large_prime(bits)
    p1, q1 = generate_large_prime(bits), generate_large_prime(bits)
    if p * q > p1 * q1:
        p, q, p1, q1 = p1, q1, p, q
    return GenerateKeyPair(p, q), GenerateKeyPair(p1, q1)


def save_keys(A, B, filename=KEYS_FILE):
    data = {}
    for name, (pub, priv) in (("A", A), ("B", B)):
        data[name] = {"n": pub[0], "e": pub[1], "d": priv[0], "p": priv[1], "q": priv[2]}
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def load_keys(filename=KEYS_FILE):
    with open(filename) as f:
        data = json.load(f)
    res = []
    for name in ("A", "B"):
        k = data[name]
        res.append(((k["n"], k["e"]), (k["d"], k["p"], k["q"])))
    return res[0], res[1]

def Encrypt(M, e, n):
    if not 0 <= M <= n - 1:
        raise ValueError("Повідомлення має бути в межах 0 <= M <= n-1")
    return mod_pow(M, e, n)

def Decrypt(C, d, n):
    return mod_pow(C, d, n)

def Sign(M, d, n):
    return mod_pow(M, d, n)

def Verify(M, S, e, n):
    return M == mod_pow(S, e, n)

def SendKey(k, d, n, e1, n1):
    if n1 < n:
        raise ValueError("n1 < n: A має згенерувати іншу пару ключів")
    if not 0 < k < n:
        raise ValueError("Потрібно 0 < k < n")
    S = Sign(k, d, n)
    k1 = Encrypt(k, e1, n1)
    S1 = Encrypt(S, e1, n1)
    return k1, S1


def ReceiveKey(k1, S1, d1, n1, e, n):
    k = Decrypt(k1, d1, n1)
    S = Decrypt(S1, d1, n1)
    return k, Verify(k, S, e, n)


def _h(x):
    return format(x, "X")


def _i(s):
    return int(s.strip().replace("0x", ""), 16)


def server_mode():
    if os.path.exists(KEYS_FILE):
        A, B = load_keys()
    else:
        A, B = build_keys(256)
        save_keys(A, B)
    me = A
    (n, e), (d, p, q) = me
    print("Ваш відкритий ключ (вставте його на сервері):")
    print("  n =", _h(n))
    print("  e =", _h(e))
    menu = """
1. Encrypt  (за відкритим ключем сервера)
2. Decrypt  (нашим секретним ключем)
3. Sign     (нашим секретним ключем)
4. Verify   (за відкритим ключем сервера)
5. SendKey  (наш -> сервер)
6. ReceiveKey (сервер -> наш)
0. Вихід"""
    while True:
        print(menu)
        c = input("> ").strip()
        try:
            if c == "1":
                ns, es = _i(input("n сервера (hex): ")), _i(input("e сервера (hex): "))
                print("C =", _h(Encrypt(_i(input("M (hex): ")), es, ns)))
            elif c == "2":
                print("M =", _h(Decrypt(_i(input("C (hex): ")), d, n)))
            elif c == "3":
                print("S =", _h(Sign(_i(input("M (hex): ")), d, n)))
            elif c == "4":
                ns, es = _i(input("n сервера (hex): ")), _i(input("e сервера (hex): "))
                M, S = _i(input("M (hex): ")), _i(input("S (hex): "))
                print("Підпис вірний:", Verify(M, S, es, ns))
            elif c == "5":
                n1, e1 = _i(input("n сервера (hex): ")), _i(input("e сервера (hex): "))
                k = _i(input("k (hex): "))
                k1, S1 = SendKey(k, d, n, e1, n1)
                print("k1 =", _h(k1))
                print("S1 =", _h(S1))
            elif c == "6":
                ns, es = _i(input("n сервера (hex, відправник): ")), _i(input("e сервера (hex): "))
                k1, S1 = _i(input("k1 (hex): ")), _i(input("S1 (hex): "))
                kk, ok = ReceiveKey(k1, S1, d, n, es, ns)
                print("k =", _h(kk), "| підпис вірний:", ok)
            elif c == "0":
                break
        except Exception as ex:
            print("Помилка:", ex)



if __name__ == "__main__":
    if "--server" in sys.argv:
        server_mode()
        sys.exit()

    print("=" * 60)
    print("ЗАВДАННЯ 1. ГЕНЕРАЦІЯ 256-БІТНОГО ПРОСТОГО ЧИСЛА")
    print("=" * 60)
    p_task1 = generate_large_prime(bits=256, verbose=True)
    print("\n--- Знайдене просте число ---")
    print(p_task1)
    miller_rabin(p_task1, k=1, debug=True)

    print("\n" + "=" * 60)
    print("ЗАВДАННЯ 2. ГЕНЕРАЦІЯ ПАР ПРОСТИХ ЧИСЕЛ ДЛЯ А ТА В")
    print("=" * 60)

    print("Генеруємо числа...")
    p = generate_large_prime(bits=256)
    q = generate_large_prime(bits=256)
    p1 = generate_large_prime(bits=256)
    q1 = generate_large_prime(bits=256)
    nA = p * q
    nB = p1 * q1
    if nA > nB:
        print("-> Увага: для виконання умови nA <= nB, пари А і В поміняні місцями.")
        p, q, p1, q1 = p1, q1, p, q
        nA, nB = nB, nA

    print("\n--- РЕЗУЛЬТАТИ ---")
    print(f"Абонент А:")
    print(f" p  = {p}")
    print(f" q  = {q}")
    print(f" nA = p*q = {nA}")

    print(f"\nАбонент В:")
    print(f" p1 = {p1}")
    print(f" q1 = {q1}")
    print(f" nB = p1*q1 = {nB}")

    print(f"\nПеревірка умови pq <= p1q1: {nA} <= {nB} -> {nA <= nB}")
    print(f"\nБітові довжини (всі мають бути 256):")
    print(f"p: {p.bit_length()}, q: {q.bit_length()}, p1: {p1.bit_length()}, q1: {q1.bit_length()}")

    print("\n" + "=" * 60)
    print("ЗАВДАННЯ 3. ГЕНЕРАЦІЯ КЛЮЧІВ RSA ДЛЯ А ТА B")
    print("=" * 60)
    A = GenerateKeyPair(p, q)
    B = GenerateKeyPair(p1, q1)
    save_keys(A, B)
    print(f"(ключі збережено у {KEYS_FILE})")
    (nA, eA), (dA, _, _) = A
    (nB, eB), (dB, _, _) = B
    print("\n--- Абонент A: параметри та перевірка ---")
    okA = check_key_pair(*A)
    print("\n--- Абонент B: параметри та перевірка ---")
    okB = check_key_pair(*B)
    print(f"\nnA <= nB: {nA <= nB}; ключі коректні: {okA and okB}")

    print("\n" + "=" * 60)
    print("ЗАВДАННЯ 4. ШИФРУВАННЯ, РОЗШИФРУВАННЯ, ПІДПИС")
    print("=" * 60)
    for name, (n, e), d in (("A", A[0], dA), ("B", B[0], dB)):
        M = random.randrange(2, n - 1)
        C = Encrypt(M, e, n)
        M2 = Decrypt(C, d, n)
        S = Sign(M, d, n)
        ok = Verify(M, S, e, n)
        print(f"\n--- Абонент {name} ---")
        print(f"M = {M}\nC = {C}\nрозшифровано = {M2}  -> збігається: {M == M2}")
        print(f"S = {S}\nпідпис вірний: {ok}")
        print(f"підпис підробленого M+1 вірний: {Verify(M + 1, S, e, n)}")

    print("\n" + "=" * 60)
    print("ЗАВДАННЯ 5. ПРОТОКОЛ КОНФІДЕНЦІЙНОГО РОЗСИЛАННЯ КЛЮЧІВ (A -> B)")
    print("=" * 60)
    k = random.randrange(1, nA)
    print(f"A обирає k (0 < k < nA) = {k}")
    S = Sign(k, dA, nA)
    print(f"A: S  = k^d mod n      = {S}")
    k1, S1 = SendKey(k, dA, nA, eB, nB)
    print(f"A: k1 = k^e1 mod n1    = {k1}")
    print(f"A: S1 = S^e1 mod n1    = {S1}")
    print("A --> B: (k1, S1)")
    kB, ok = ReceiveKey(k1, S1, dB, nB, eA, nA)
    print(f"B: k  = k1^d1 mod n1   = {kB}")
    print(f"B: S  = S1^d1 mod n1   = {Decrypt(S1, dB, nB)}")
    print(f"B: перевірка k == S^e mod n: {ok}")
    print(f"Ключ отримано коректно: {kB == k}")
    print("\nДля перевірки на тестовому сервері: python <ім'я_файлу>.py --server")
