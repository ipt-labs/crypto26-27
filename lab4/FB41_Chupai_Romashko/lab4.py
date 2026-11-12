"""
КП №4. RSA. Завдання 1: генерація випадкових простих чисел
(пробні ділення + тест Міллера-Рабіна, реалізовані власноруч).
"""
import argparse
import json
import os
import random



# Допоміжні функції 

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def power_mod(x, e, m):
    y = 1
    for bit in bin(e)[2:]:
        y = y * y % m
        if bit == "1":
            y = y * x % m
    return y


def small_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i, is_p in enumerate(sieve) if is_p]


SMALL_PRIMES = small_primes(1000)     # 168 малих простих чисел для пробних ділень


# Пробні ділення 

def trial_division(n):
    for q in SMALL_PRIMES:
        if n == q:
            return None
        if n % q == 0:
            return q
    return None


# Тест Міллера-Рабіна 

def decompose(p):
    d, s = p - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    return s, d


def strong_pseudoprime(p, x, trace=None):
    s, d = decompose(p)
    xr = power_mod(x, d, p)                 
    if trace is not None:
        trace.append((0, xr))
    if xr == 1 or xr == p - 1:
        return True
    for r in range(1, s):
        xr = xr * xr % p                     
        if trace is not None:
            trace.append((r, xr))
        if xr == p - 1:
            return True                      
        if xr == 1:
            return False                     
    return False


def miller_rabin(p, rounds=20):
    for _ in range(rounds):
        x = random.randint(2, p - 2)
        if gcd(x, p) != 1:
            return False, x
        if not strong_pseudoprime(p, x):
            return False, x
    return True, None


def is_prime(n, rounds=20):
    if n < 2:
        return False
    if n <= SMALL_PRIMES[-1]:
        return n in SMALL_PRIMES
    if trial_division(n) is not None:
        return False
    return miller_rabin(n, rounds)[0]

# Генерація випадкового простого числа

def random_prime(bits, rounds=20, log=None):
    n0, n1 = 2 ** (bits - 1), 2 ** bits - 1
    if log is not None:
        log.update({"start": None, "tested": 0, "trial": [], "mr": []})
    while True:
        x = random.randint(n0, n1)
        m = x if x % 2 == 1 else x + 1
        if log is not None and log["start"] is None:
            log["start"] = x
        while m <= n1:
            if log is not None:
                log["tested"] += 1
            q = trial_division(m)
            if q is not None:
                if log is not None:
                    log["trial"].append((m, q))
            else:
                ok, witness = miller_rabin(m, rounds)
                if ok:
                    return m
                if log is not None:
                    log["mr"].append((m, witness))
            m += 2

# Завдання 2: дві пари простих чисел
 
def generate_primes_for_two_users(bits=256, rounds=20):
    nums, logs = [], []
    while len(nums) < 4:
        log = {}
        x = random_prime(bits, rounds, log)
        if x in nums:                       # усі чотири числа мають бути різними
            continue
        log["prime"] = x
        nums.append(x)
        logs.append(log)
    pair_a, pair_b = (nums[0], nums[1]), (nums[2], nums[3])
    logs_a, logs_b = logs[0:2], logs[2:4]
    if pair_a[0] * pair_a[1] > pair_b[0] * pair_b[1]:     # А має отримати меншу пару
        pair_a, pair_b = pair_b, pair_a
        logs_a, logs_b = logs_b, logs_a
    (p, q), (p1, q1) = pair_a, pair_b
    return p, q, p1, q1, logs_a + logs_b
 

 # Завдання 3: генерація ключових пар RSA 
 
def egcd(a, b):
    u0, u1, v0, v1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return a, u0, v0
 
 
def inv(a, n):
    d, u, _ = egcd(a % n, n)
    return u % n if d == 1 else None
 
 
def generate_key_pair(p, q, e=65537):
    n = p * q
    phi = (p - 1) * (q - 1)                 # функція Ойлера phi(n)
    if gcd(e, phi) != 1:                    # e = 2^16 + 1 може не підійти; тоді беремо випадкове e
        while True:
            e = random.randrange(3, phi - 1, 2)
            if gcd(e, phi) == 1:
                break
    d = inv(e, phi)                         # e*d = 1 (mod phi(n))
    return (n, e), (d, p, q)
 
 
def check_key_pair(public, secret):
    n, e = public
    d, p, q = secret
    phi = (p - 1) * (q - 1)
    m = random.randrange(2, n - 1)          # випадкове повідомлення
    return [
        ("p і q прості (тест Міллера-Рабіна)", is_prime(p) and is_prime(q)),
        ("p != q", p != q),
        ("n = p*q", n == p * q),
        ("1 < e < phi(n)", 1 < e < phi),
        ("gcd(e, phi(n)) = 1", gcd(e, phi) == 1),
        ("0 < d < phi(n)", 0 < d < phi),
        ("e*d = 1 (mod phi(n))", e * d % phi == 1),
        ("розшифрування: (M^e)^d mod n = M", power_mod(power_mod(m, e, n), d, n) == m),
        ("підпис: (M^d)^e mod n = M", power_mod(power_mod(m, d, n), e, n) == m),
    ]
 
 
def save_keys(path, keys):
    data = {name: {"public": {"n": str(pub[0]), "e": str(pub[1])},
                   "secret": {"d": str(sec[0]), "p": str(sec[1]), "q": str(sec[2])}}
            for name, (pub, sec) in keys.items()}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
 
def load_keys(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {name: ((int(v["public"]["n"]), int(v["public"]["e"])),
                   (int(v["secret"]["d"]), int(v["secret"]["p"]), int(v["secret"]["q"])))
            for name, v in data.items()}
 
 
def load_primes(path="primes.json"):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return int(d["p"]), int(d["q"]), int(d["p1"]), int(d["q1"])
 
 
# Демонстрація
 
def task1():
    BITS = 256
    log = {}
    p = random_prime(BITS, log=log)
 
    print(f"Генерація випадкового простого числа довжиною {BITS} біт")
    print(f"Початкове випадкове число x:\n  {log['start']}")
    print(f"Перевірено непарних кандидатів: {log['tested']}")
    print(f"  відхилено пробними діленнями:     {len(log['trial'])}")
    print(f"  відхилено тестом Міллера-Рабіна:  {len(log['mr'])}")
 
    print("\nПерші 3 кандидати, відхилені пробними діленнями (число, дільник):")
    for m, q in log["trial"][:3]:
        print(f"  {m}\n    ділиться на {q}")
 
    print("\nКандидати, відхилені тестом Міллера-Рабіна (число, основа-свідок):")
    for m, x in log["mr"]:
        print(f"  {m}\n    основа x = {x}")
 
    print(f"\nЗнайдене просте число p ({p.bit_length()} біт):\n  {p}")
 
    # Проміжні результати тесту Міллера-Рабіна для однієї з основ
    s, d = decompose(p)
    x = random.randint(2, p - 2)
    trace = []
    result = strong_pseudoprime(p, x, trace)
    print("\nПроміжні результати тесту Міллера-Рабіна для p:")
    print(f"  p - 1 = 2^{s} * d, де d = {d}")
    print(f"  основа x = {x}, gcd(x, p) = {gcd(x, p)}")
    for r, val in trace:
        mark = "  (= 1)" if val == 1 else "  (= -1 mod p)" if val == p - 1 else ""
        print(f"  r = {r}: x^(2^{r} * d) mod p = {val}{mark}")
    print(f"  p сильно псевдопросте за основою x: {result}")
 
 
def task2():
    BITS = 256
    if os.path.exists("primes.json"):
        p, q, p1, q1 = load_primes("primes.json")
        print("Числа вже згенеровано раніше й збережено у primes.json (щоб отримати нові, видаліть цей файл):\n")
        for name, owner, num in zip(["p", "q", "p1", "q1"], ["А", "А", "B", "B"], (p, q, p1, q1)):
            print(f"{name} (абонент {owner}, {num.bit_length()} біт):\n  {num}")
        print(f"\nn = p*q ({(p * q).bit_length()} біт), n1 = p1*q1 ({(p1 * q1).bit_length()} біт)")
        print(f"Умова p*q <= p1*q1 виконується: {p * q <= p1 * q1}")
        return
    p, q, p1, q1, logs = generate_primes_for_two_users(BITS)
    names = ["p", "q", "p1", "q1"]
    owners = ["А", "А", "B", "B"]
 
    print(f"Чотири прості числа довжиною {BITS} біт\n")
    for name, owner, num, lg in zip(names, owners, (p, q, p1, q1), logs):
        print(f"{name} (абонент {owner}, {num.bit_length()} біт):\n  {num}")
        print(f"  кандидатів перевірено: {lg['tested']}, відхилено пробними діленнями: {len(lg['trial'])}, "
              f"відхилено тестом Міллера-Рабіна: {len(lg['mr'])}")
 
    n, n1 = p * q, p1 * q1
    print(f"\nn = p*q ({n.bit_length()} біт):\n  {n}")
    print(f"n1 = p1*q1 ({n1.bit_length()} біт):\n  {n1}")
    print(f"Умова p*q <= p1*q1 виконується: {n <= n1}")
 
    # повний перелік відхилених кандидатів - для додатка до звіту
    with open("primes_log.txt", "w", encoding="utf-8") as f:
        for name, num, lg in zip(names, (p, q, p1, q1), logs):
            f.write(f"=== {name} = {num}\n")
            f.write(f"Початкове x: {lg['start']}\n")
            f.write(f"Відхилено пробними діленнями ({len(lg['trial'])}): число, малий дільник\n")
            for m, d in lg["trial"]:
                f.write(f"  {m}  ділиться на {d}\n")
            f.write(f"Відхилено тестом Міллера-Рабіна ({len(lg['mr'])}): число, основа-свідок\n")
            for m, x in lg["mr"]:
                f.write(f"  {m}  основа {x}\n")
            f.write("\n")
    with open("primes.json", "w", encoding="utf-8") as f:
        json.dump({"p": str(p), "q": str(q), "p1": str(p1), "q1": str(q1)}, f, indent=2)
    print("\nПовний перелік відхилених кандидатів збережено у primes_log.txt, числа у primes.json")
 
 
def task3():
    if not os.path.exists("primes.json"):
        print("Спочатку виконайте завдання 2: python3 lab4.py 2")
        return
    p, q, p1, q1 = load_primes("primes.json")
    keys = {"A": generate_key_pair(p, q), "B": generate_key_pair(p1, q1)}
    save_keys("keys.json", keys)
 
    (n, e), (d, _, _) = keys["A"][0], keys["A"][1]
    phi = (p - 1) * (q - 1)
    print("Абонент А: параметри RSA")
    print(f"  p = {p}")
    print(f"  q = {q}")
    print(f"  n = p*q = {n}  ({n.bit_length()} біт)")
    print(f"  phi(n) = (p-1)(q-1) = {phi}")
    print(f"  e = {e}  (2^16 + 1)" if e == 65537 else f"  e = {e}")
    print(f"  d = e^(-1) mod phi(n) = {d}")
 
    print("\nАбонент B: параметри RSA")
    (n1, e1), (d1, _, _) = keys["B"][0], keys["B"][1]
    print(f"  p1 = {p1}")
    print(f"  q1 = {q1}")
    print(f"  n1 = p1*q1 = {n1}  ({n1.bit_length()} біт)")
    print(f"  e1 = {e1}")
    print(f"  d1 = {d1}")
 
    for name in ("A", "B"):
        print(f"\nПеревірка співвідношень RSA для абонента {name}:")
        for text, ok in check_key_pair(*keys[name]):
            print(f"  [{'так' if ok else 'НІ'}] {text}")
    print(f"\nУмова n <= n1 (потрібна для протоколу розсилання ключів): {n <= n1}")
    print("Ключі збережено у keys.json (відкриті: n, e; секретні: d, p, q)")
 
 

# Завдання 4: шифрування, розшифрування, підпис, перевірка підпису
# Кожна процедура приймає ЛИШЕ ті дані, які потрібні для її виконання.
# (GenerateKeyPair() реалізована вище як generate_key_pair)

def encrypt(m, e, n):
    """Шифрування: повідомлення та ВІДКРИТИЙ ключ адресата (e, n)."""
    if not 0 <= m <= n - 1:
        raise ValueError("повідомлення має задовольняти 0 <= M <= n-1")
    return power_mod(m, e, n)


def decrypt(c, d, n):
    """Розшифрування: криптограма та СЕКРЕТНИЙ ключ d (і модуль n)."""
    if not 0 <= c <= n - 1:
        raise ValueError("криптограма має задовольняти 0 <= C <= n-1")
    return power_mod(c, d, n)


def sign(m, d, n):
    """Створення підпису S = M^d mod n: повідомлення та СЕКРЕТНИЙ ключ d (і n)."""
    if not 0 <= m <= n - 1:
        raise ValueError("повідомлення має задовольняти 0 <= M <= n-1")
    return power_mod(m, d, n)


def verify(m, s, e, n):
    """Перевірка підпису: M, S та ВІДКРИТИЙ ключ відправника (e, n)."""
    if not 0 <= s <= n - 1:
        return False
    return power_mod(s, e, n) == m % n


def get_users(path="keys.json"):
    keys = load_keys(path)
    (n, e), (d, _, _) = keys["A"]
    (n1, e1), (d1, _, _) = keys["B"]
    return {"A": {"n": n, "e": e, "d": d}, "B": {"n": n1, "e": e1, "d": d1}}


def task4():
    if not os.path.exists("keys.json"):
        print("Спочатку виконайте завдання 3: python3 lab4.py 3")
        return
    users = get_users()
    for name in ("A", "B"):
        n, e, d = users[name]["n"], users[name]["e"], users[name]["d"]
        print(f"===== Абонент {name} =====")
        print(f"n = {n}\ne = {e}\nd = {d}\n")

        m = random.randrange(2, n - 1)                  # випадкове відкрите повідомлення
        print(f"Відкрите повідомлення M:\n  {m}")
        c = encrypt(m, e, n)
        print(f"Криптограма C = M^e mod n:\n  {c}")
        m2 = decrypt(c, d, n)
        print(f"Розшифрування M' = C^d mod n:\n  {m2}")
        print(f"  M' == M: {m2 == m}\n")

        s = sign(m, d, n)
        print(f"Цифровий підпис S = M^d mod n:\n  {s}")
        print(f"  Підпис вірний (M == S^e mod n): {verify(m, s, e, n)}")
        print(f"  Спотворене повідомлення (M+1) приймається: {verify(m + 1, s, e, n)}")
        print(f"  Спотворений підпис (S+1) приймається:      {verify(m, s + 1, e, n)}\n")


# Завдання 5: протокол конфіденційного розсилання ключів

def send_key(k, d, n, e1, n1):
    """
    Сторона відправника А.
    Вхід: секрет k, СЕКРЕТНИЙ ключ А (d, n), ВІДКРИТИЙ ключ B (e1, n1).
    Вихід: (k1, S1, S): S = k^d mod n, k1 = k^e1 mod n1, S1 = S^e1 mod n1.
    """
    if n1 < n:
        raise ValueError("n1 < n: абонент А має згенерувати собі іншу пару ключів")
    if not 0 < k < n:
        raise ValueError("потрібно 0 < k < n")
    s = sign(k, d, n)            # підпис на секретному ключі А
    k1 = encrypt(k, e1, n1)      # шифрування на відкритому ключі B
    s1 = encrypt(s, e1, n1)      # шифрування підпису на відкритому ключі B
    return k1, s1, s


def receive_key(k1, s1, d1, n1, e, n):
    """
    Сторона одержувача B.
    Вхід: (k1, S1), СЕКРЕТНИЙ ключ B (d1, n1), ВІДКРИТИЙ ключ А (e, n).
    Вихід: (k, S, ok): k = k1^d1 mod n1, S = S1^d1 mod n1, ok = (k == S^e mod n).
    """
    k = decrypt(k1, d1, n1)      # конфіденційність
    s = decrypt(s1, d1, n1)
    ok = verify(k, s, e, n)      # автентифікація
    return k, s, ok


def task5():
    if not os.path.exists("keys.json"):
        print("Спочатку виконайте завдання 3: python3 lab4.py 3")
        return
    users = get_users()
    n, e, d = users["A"]["n"], users["A"]["e"], users["A"]["d"]
    n1, e1, d1 = users["B"]["n"], users["B"]["e"], users["B"]["d"]

    print("Протокол конфіденційного розсилання ключів (А -> B)")
    print(f"Умова n1 >= n: {n1 >= n}\n")
    print(f"Відкритий ключ А:  n  = {n}\n                   e  = {e}")
    print(f"Відкритий ключ B:  n1 = {n1}\n                   e1 = {e1}\n")

    k = random.randrange(1, n)                          # 0 < k < n
    print(f"Секрет k (0 < k < n), який передає А:\n  {k}\n")

    k1, s1, s = send_key(k, d, n, e1, n1)
    print("--- Абонент А обчислює ---")
    print(f"S  = k^d mod n   (підпис на секретному ключі d А):\n  {s}")
    print(f"k1 = k^e1 mod n1 (шифрування на відкритому ключі e1 B):\n  {k1}")
    print(f"S1 = S^e1 mod n1 (шифрування підпису на e1 B):\n  {s1}")
    print("\n--- По відкритому каналу передається (k1, S1) ---\n")

    k_b, s_b, ok = receive_key(k1, s1, d1, n1, e, n)
    print("--- Абонент B обчислює ---")
    print(f"k = k1^d1 mod n1 (розшифрування на секретному ключі d1 B):\n  {k_b}")
    print(f"S = S1^d1 mod n1:\n  {s_b}")
    print(f"S^e mod n (перевірка на відкритому ключі e А):\n  {power_mod(s_b, e, n)}")
    print(f"\nПідпис вірний (k == S^e mod n): {ok}")
    print(f"Отриманий k збігається з надісланим: {k_b == k}")
    _, _, ok_bad = receive_key(k1, (s1 + 1) % n1, d1, n1, e, n)
    print(f"Спотворений S1 приймається одержувачем: {ok_bad}")


# Інструменти для перевірки з тестовим середовищем (числа в hex, без 0x)

def hx(x):
    return format(x, "X")


def parse_hex(s):
    return int(s.strip().replace(" ", ""), 16)


def tool(args):
    users = get_users()
    who = users[args.user]
    if args.task == "show":
        print(f"Modulus (n), hex:\n{hx(who['n'])}\nPublic exponent (e), hex:\n{hx(who['e'])}")
    elif args.task == "enc":
        print(hx(encrypt(parse_hex(args.m), parse_hex(args.e), parse_hex(args.n))))
    elif args.task == "dec":
        print(hx(decrypt(parse_hex(args.c), who["d"], who["n"])))
    elif args.task == "sign":
        print(hx(sign(parse_hex(args.m), who["d"], who["n"])))
    elif args.task == "verify":
        print(verify(parse_hex(args.m), parse_hex(args.s), parse_hex(args.e), parse_hex(args.n)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="КП №4. RSA")
    ap.add_argument("task", nargs="?",
                    choices=["1", "2", "3", "4", "5", "show", "enc", "dec", "sign", "verify"],
                    help="номер завдання або інструмент для тестового середовища")
    ap.add_argument("--user", choices=["A", "B"], default="A", help="чиї ключі використати")
    ap.add_argument("--m"), ap.add_argument("--c"), ap.add_argument("--s")
    ap.add_argument("--n"), ap.add_argument("--e")
    args = ap.parse_args()

    if args.task in ("show", "enc", "dec", "sign", "verify"):
        tool(args)
    else:
        tasks = {1: task1, 2: task2, 3: task3, 4: task4, 5: task5}
        for number in ([int(args.task)] if args.task else [1, 2, 3, 4, 5]):
            if not args.task and number > 1:
                print("\n" + "=" * 70 + "\n")
            tasks[number]()