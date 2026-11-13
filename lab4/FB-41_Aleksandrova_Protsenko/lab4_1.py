import json
import random

# ----------------------------------------------------------------------
# Базова арифметика
# ----------------------------------------------------------------------

def modpow(a, b, m):
    """Швидке піднесення до степеня a^b mod m (схема Горнера, зліва направо)."""
    y = 1
    for bit in bin(b)[2:]:          # старші біти -> молодші
        y = (y * y) % m
        if bit == '1':
            y = (y * a) % m
    return y


def gcd(a, b):
    """Алгоритм Евкліда."""
    while b:
        a, b = b, a % b
    return a


def egcd(a, b):
    """Розширений алгоритм Евкліда: повертає (g, x, y), де a*x + b*y = g."""
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def modinv(a, m):
    """Обернений елемент a^(-1) mod m."""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("Оберненого елемента не існує (gcd != 1)")
    return x % m


# ----------------------------------------------------------------------
# Тести на простоту
# ----------------------------------------------------------------------

SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def trial_division(n):
    """
    Пробні ділення на малі прості.
    Повертає (True, None), якщо n пройшло перевірку,
    або (False, p), де p - малий дільник, що відкинув n.
    """
    for p in SMALL_PRIMES:
        if n == p:
            return True, None
        if n % p == 0:
            return False, p
    return True, None


def is_strong_pseudoprime(p, d, s, x, verbose=False):
    """
    Чи є p сильно псевдопростим за основою x (p - 1 = d * 2^s).
    Кроки 2.1 - 2.3 з описа тесту Міллера-Рабіна.
    """
    xr = modpow(x, d, p)
    if verbose:
        print(f"    x^d mod p = {xr}   (r = 0)")
    if xr == 1 or xr == p - 1:
        if verbose:
            print("    x^d mod p = ±1  =>  p сильно псевдопросте за цією основою")
        return True
    for r in range(1, s):
        xr = (xr * xr) % p
        if verbose:
            print(f"    x_{r} = x_{r-1}^2 mod p = {xr}")
        if xr == p - 1:
            if verbose:
                print(f"    x_{r} = -1  =>  p сильно псевдопросте за цією основою")
            return True
        if xr == 1:
            if verbose:
                print(f"    x_{r} = 1  =>  p НЕ сильно псевдопросте")
            return False
    if verbose:
        print("    -1 не знайдено  =>  p НЕ сильно псевдопросте")
    return False


def miller_rabin(p, k=20, verbose=False):
    """
    Імовірнісний тест Міллера-Рабіна з k випадковими основами.
    Повертає (True, None) або (False, x), де x - основа-свідок складеності.
    Якщо verbose=True, то для ПЕРШОЇ основи друкуються проміжні результати.
    """
    if p < 2:
        return False, None
    if p in (2, 3):
        return True, None
    if p % 2 == 0:
        return False, 2

    # Крок 0: p - 1 = d * 2^s, d непарне
    d, s = p - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    if verbose:
        print(f"  p = {p}")
        print(f"  p - 1 = d * 2^s,  s = {s},  d = {d}")

    for i in range(k):
        # Крок 1: x з інтервалу 1 < x < p
        x = random.randint(2, p - 1)
        g = gcd(x, p)
        show = verbose and i == 0
        if show:
            print(f"  Основа x = {x},  gcd(x, p) = {g}")
        if g > 1:
            return False, x
        # Крок 2: чи сильно псевдопросте за основою x
        if not is_strong_pseudoprime(p, d, s, x, verbose=show):
            return False, x
    return True, None


# ----------------------------------------------------------------------
# Генерація простих чисел (п.1)
# ----------------------------------------------------------------------

def gen_prime(bits, k=20, rejected=None):
    """
    Випадкове просте число довжиною рівно `bits` біт.
    rejected - список, куди записуються кандидати, що не пройшли тести:
               елементи (кандидат, причина).
    """
    if rejected is None:
        rejected = []
    while True:
        x = random.getrandbits(bits)
        x |= (1 << (bits - 1))      # старший біт = 1  -> рівно `bits` біт
        x |= 1                      # непарне
        while x.bit_length() == bits:
            ok, div = trial_division(x)
            if not ok:
                rejected.append((x, f"пробні ділення: ділиться на {div}"))
            else:
                ok, witness = miller_rabin(x, k)
                if ok:
                    return x
                rejected.append((x, f"Міллер-Рабін: основа {witness}"))
            x += 2                  # наступне непарне число
        # вийшли за межі довжини - починаємо з нового випадкового x

def two_adic(n):
    """Показник s у розкладі n = d * 2^s (d непарне)."""
    s = 0
    while n % 2 == 0:
        n //= 2
        s += 1
    return s


# ----------------------------------------------------------------------
# Генерація p, q, p1, q1 (п.2)
# ----------------------------------------------------------------------

def generate_primes_for_AB(bits=256, k=20):
    """
    Повертає (p, q, p1, q1, rejected) з умовою p*q <= p1*q1.
    (p, q) - для абонента A, (p1, q1) - для абонента B.
    """
    rejected = {"p": [], "q": [], "p1": [], "q1": []}

    def distinct_pair(name1, name2):
        a = gen_prime(bits, k, rejected[name1])
        b = gen_prime(bits, k, rejected[name2])
        while b == a:
            b = gen_prime(bits, k, rejected[name2])
        return a, b

    p, q = distinct_pair("p", "q")
    p1, q1 = distinct_pair("p1", "q1")

    if p * q > p1 * q1:             # міняємо пари місцями
        p, q, p1, q1 = p1, q1, p, q
        rejected["p"], rejected["p1"] = rejected["p1"], rejected["p"]
        rejected["q"], rejected["q1"] = rejected["q1"], rejected["q"]
    return p, q, p1, q1, rejected


# ----------------------------------------------------------------------
# Ключі RSA (п.3)
# ----------------------------------------------------------------------

def GenerateKeyPair(p, q, e=None):
    """
    Повертає (public, private):
        public  = (n, e)
        private = (d, p, q)
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    if e is None:
        e = 2 ** 16 + 1
    while not (2 <= e <= phi - 1 and gcd(e, phi) == 1):
        e = random.randint(2, phi - 1)
    d = modinv(e, phi)
    return (n, e), (d, p, q)


def check_key(public, private, name="", verbose=True):
    """Перевірка співвідношень, потрібних для коректної роботи RSA."""
    n, e = public
    d, p, q = private
    phi = (p - 1) * (q - 1)
    M = random.randint(2, n - 2)
    C = modpow(M, e, n)
    checks = {
        "p * q == n": p * q == n,
        "gcd(e, phi(n)) == 1": gcd(e, phi) == 1,
        "e * d ≡ 1 (mod phi(n))": (e * d) % phi == 1,
        "(M^e)^d ≡ M (mod n)": modpow(C, d, n) == M,
    }
    if verbose:
        print(f"--- Параметри ключа {name} ---")
        print(f"p      = {p}")
        print(f"q      = {q}")
        print(f"n      = {n}   ({n.bit_length()} біт)")
        print(f"phi(n) = {phi}")
        print(f"e      = {e}")
        print(f"d      = {d}")
        print(f"Тест: M = {M}\n      C = M^e mod n = {C}\n      C^d mod n = {modpow(C, d, n)}")
        for text, res in checks.items():
            print(f"  {text}: {'OK' if res else 'ПОМИЛКА'}")
    return all(checks.values())


def save_keys(filename, public, private):
    n, e = public
    d, p, q = private
    with open(filename, "w") as f:
        json.dump({"n": hex(n), "e": hex(e), "d": hex(d),
                   "p": hex(p), "q": hex(q)}, f, indent=2)


def load_keys(filename):
    with open(filename) as f:
        j = json.load(f)
    n, e, d, p, q = (int(j[k], 16) for k in ("n", "e", "d", "p", "q"))
    return (n, e), (d, p, q)


# ----------------------------------------------------------------------
# Демонстрація
# ----------------------------------------------------------------------

def main():
    BITS = 256

    # Самоперевірка власного modpow
    for _ in range(200):
        a = random.getrandbits(300)
        b = random.getrandbits(300)
        m = random.getrandbits(300) | 1
        assert modpow(a, b, m) == pow(a, b, m)
    print("modpow збігається з вбудованим pow: OK\n")

    # п.2 - генерація p, q, p1, q1
    print("\n=== П.2. Генерація простих чисел ===")
    p, q, p1, q1, rejected = generate_primes_for_AB(BITS)
    print(f"p  = {p}\nq  = {q}\np1 = {p1}\nq1 = {q1}")
    print(f"p*q <= p1*q1: {p * q <= p1 * q1}")

    # п.1 (доповнення) - проміжні результати Міллера-Рабіна для одного
    # зі згенерованих простих чисел (обираємо те, де s >= 2, найменше таке,
    # щоб ланцюжок квадратів було видно, але вивід був компактним)
    named = {"p": p, "q": q, "p1": p1, "q1": q1}
    candidates = {nm: two_adic(v - 1) for nm, v in named.items()}
    good = {nm: s for nm, s in candidates.items() if s >= 2}
    name = min(good, key=good.get) if good else max(candidates, key=candidates.get)
    print(f"\n=== П.1. Проміжні результати тесту Міллера-Рабіна для числа {name} ===")
    miller_rabin(named[name], k=1, verbose=True)

    with open("rejected_candidates.txt", "w", encoding="utf-8") as f:
        for name, lst in rejected.items():
            f.write(f"=== Кандидати для {name}: відкинуто {len(lst)} ===\n")
            for cand, reason in lst:
                f.write(f"{cand}  <- {reason}\n")
            f.write("\n")
    print("Відкинуті кандидати (кількість):",
          {k: len(v) for k, v in rejected.items()},
          "-> файл rejected_candidates.txt")

    # п.3 - ключі
    print("\n=== П.3. Ключові пари RSA ===")
    pubA, privA = GenerateKeyPair(p, q)
    pubB, privB = GenerateKeyPair(p1, q1)
    assert check_key(pubA, privA, "A")
    assert check_key(pubB, privB, "B")
    print(f"\nn1 >= n (потрібно для протоколу): {pubB[0] >= pubA[0]}")

    save_keys("keys_A.json", pubA, privA)
    save_keys("keys_B.json", pubB, privB)
    print("Ключі збережено у keys_A.json та keys_B.json")


if __name__ == "__main__":
    main()
