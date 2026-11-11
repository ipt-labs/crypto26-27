import json
from math import gcd


def GenerateKeyPair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    while gcd(e, phi) != 1:
        e += 2
    d = pow(e, -1, phi)
    return (n, e), (d, p, q)

def main():
    with open("primes.json", encoding="utf-8") as f:
        primes = json.load(f)

    keys = {}
    for name, p, q in (
        ("A", primes["p"], primes["q"]),
        ("B", primes["p1"], primes["q1"])
    ):
        public, private = GenerateKeyPair(p, q)
        n, e = public
        d, p, q = private
        phi = (p - 1) * (q - 1)
        keys[name] = {
            "public": {"n": n, "e": e},
            "private": {"d": d, "p": p, "q": q}
        }
        print(f"Абонент {name}:")
        print(f"p = {p}")
        print(f"q = {q}")
        print(f"n = {n}")
        print(f"Довжина n: {n.bit_length()} біт")
        print(f"phi(n) = {phi}")
        print(f"e = {e}")
        print(f"d = {d}")
        print("\nПеревірка співвідношень RSA:")
        print(f"p != q: {p != q}")
        print(f"n = p * q: {n == p * q}")
        print(f"1 < e < phi(n): {1 < e < phi}")
        print(f"НСД(e, phi(n)) = {gcd(e, phi)}")
        print(f"(e * d) mod phi(n) = {(e * d) % phi}")
        print()
    with open("keys.json", "w", encoding="utf-8") as f:
        json.dump(keys, f, indent=4)
    print("Ключі абонентів A і B збережено у keys.json")
    
if __name__ == "__main__":
    main()
