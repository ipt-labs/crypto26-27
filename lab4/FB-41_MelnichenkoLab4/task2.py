import json
from task1 import generate_prime


def main():
    primes = []
    while len(primes) < 4:
        p, _, _ = generate_prime(256)
        if p not in primes:
            primes.append(p)
    p, q, p1, q1 = primes
    if p * q > p1 * q1:
        p, q, p1, q1 = p1, q1, p, q
    print("Прості числа абонента А:")
    print(f"p = {p}")
    print(f"Довжина p: {p.bit_length()} біт")
    print(f"q = {q}")
    print(f"Довжина q: {q.bit_length()} біт")
    print("\nПрості числа абонента B:")
    print(f"p1 = {p1}")
    print(f"Довжина p1: {p1.bit_length()} біт")
    print(f"q1 = {q1}")
    print(f"Довжина q1: {q1.bit_length()} біт")
    print(f"\np * q = {p * q}")
    print(f"p1 * q1 = {p1 * q1}")
    print(f"Умова p * q <= p1 * q1: {p * q <= p1 * q1}")
    with open("primes.json", "w", encoding="utf-8") as f:
        json.dump({"p": p, "q": q, "p1": p1, "q1": q1}, f, indent=4)
    print("\nЧисла збережено у primes.json")

if __name__ == "__main__":
    main()
