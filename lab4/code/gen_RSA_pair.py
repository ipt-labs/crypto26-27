import json
import os
import random
import sys
from math import gcd
from gen_prime_pair import *


PRIMES_A = (5719432018136658608641415862385035573715633676874935083451954427735197923894271, 986027933267452592690961830617824859483560305969500371712239312582560711612137)
PRIMES_B = (20037748905749184764916086119014059324577466278174296580711187559527463307287149, 27417784848910155377945431856731242786173052203351328855996192646207384279707859)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_FILES = {"A": os.path.join(BASE_DIR, "key_A.json"),
             "B": os.path.join(BASE_DIR, "key_B.json")}


def GenerateKeyPair(prime_pair):
    p, q = prime_pair
    if p == q:
        raise ValueError("Числа p і q мають бути різними.")
    if not (Miller_Rabin(p) and Miller_Rabin(q)):
        raise ValueError("Числа p і q мають бути простими.")

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 2**16 + 1
    if gcd(e, phi_n) != 1:
        raise ValueError("Порушено умову gcd(e, phi(n)) = 1: потрібно обрати інші p і q.")
    d = pow(e, -1, phi_n)

    return (d, p, q), (n, e)


def SaveKeyPair(path, key_pair):
    (d, p, q), (n, e) = key_pair
    data = {
        "public":  {"n": f"{n:x}", "e": f"{e:x}"},
        "private": {"d": f"{d:x}", "p": f"{p:x}", "q": f"{q:x}"},
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def LoadKeyPair(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    n, e = int(data["public"]["n"], 16), int(data["public"]["e"], 16)
    d, p, q = (int(data["private"][name], 16) for name in ("d", "p", "q"))
    if n != p * q:
        raise ValueError(f"Файл {path} пошкоджено: n != p * q.")
    return (d, p, q), (n, e)


def GetKeyPairs():
    pairs = []
    for name, primes in (("A", PRIMES_A), ("B", PRIMES_B)):
        path = KEY_FILES[name]
        if os.path.exists(path):
            pairs.append(LoadKeyPair(path))
        else:
            key_pair = GenerateKeyPair(primes)
            SaveKeyPair(path, key_pair)
            pairs.append(key_pair)
    return pairs


def CheckKeyPair(name, key_pair):
    (d, p, q), (n, e) = key_pair
    phi_n = (p - 1) * (q - 1)
    m = random.randint(2, n - 2)

    checks = [
        ("p, q - прості числа (Міллер-Рабін)",      Miller_Rabin(p) and Miller_Rabin(q)),
        ("p != q",                                   p != q),
        ("n = p * q",                                n == p * q),
        ("gcd(e, phi(n)) = 1",                       gcd(e, phi_n) == 1),
        ("2 <= e <= phi(n) - 1",                     2 <= e <= phi_n - 1),
        ("d * e = 1 (mod phi(n))",                   (d * e) % phi_n == 1),
        ("0 < d < phi(n)",                           0 < d < phi_n),
        ("(M^e)^d mod n = M для випадкового M",      pow(pow(m, e, n), d, n) == m),
    ]
    print(f"\nПеревірка співвідношень для ключів абонента {name} (довжина n: {n.bit_length()} біт, p: {p.bit_length()} біт, q: {q.bit_length()} біт):")
    for text, ok in checks:
        print(f"  {text}: {ok}")
    return all(ok for _, ok in checks)


if __name__ == "__main__":
    # python gen_RSA_pair.py            - ключі для простих чисел PRIMES_A, PRIMES_B
    # python gen_RSA_pair.py new [біти] - спершу генеруються нові прості числа (за замовчуванням 256 біт)
    if len(sys.argv) > 1 and sys.argv[1] == "new":
        size = int(sys.argv[2]) if len(sys.argv) > 2 else 256
        a, b = generate_rsa_primes(size)
    else:
        a, b = PRIMES_A, PRIMES_B

    key_pair_A = GenerateKeyPair(a)
    key_pair_B = GenerateKeyPair(b)

    print("Пара ключів A:", key_pair_A)
    print(f"d * e mod phi(n) = {(key_pair_A[0][0] * key_pair_A[1][1]) % ((key_pair_A[0][1] - 1) * (key_pair_A[0][2] - 1))}")

    print("Пара ключів B:", key_pair_B)
    print(f"d * e mod phi(n) = {(key_pair_B[0][0] * key_pair_B[1][1]) % ((key_pair_B[0][1] - 1) * (key_pair_B[0][2] - 1))}")

    ok_A = CheckKeyPair("A", key_pair_A)
    ok_B = CheckKeyPair("B", key_pair_B)
    print(f"\nУмова p*q <= p1*q1 (n <= n1): {key_pair_A[1][0] <= key_pair_B[1][0]}")

    if ok_A and ok_B and key_pair_A[1][0] <= key_pair_B[1][0]:
        SaveKeyPair(KEY_FILES["A"], key_pair_A)
        SaveKeyPair(KEY_FILES["B"], key_pair_B)
        print(f"\nКлючі збережено: {os.path.basename(KEY_FILES['A'])}, {os.path.basename(KEY_FILES['B'])}")
