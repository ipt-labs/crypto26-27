import random

def miller_rabin(n, rounds=32):
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    trace = None

    for i in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        values = [x]

        if x != 1 and x != n - 1:
            for _ in range(s - 1):
                x = x * x % n
                values.append(x)
                if x == n - 1:
                    break
            else:
                return False, None

        if i == 0:
            trace = (s, d, a, values)

    return True, trace

def generate_prime(bits=256):
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    rejected = []
    while True:
        n = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        divisor = next(
            (p for p in small_primes if n != p and n % p == 0),
            None
        )
        if divisor is not None:
            rejected.append((n, f"ділиться на {divisor}"))
            continue
        passed, trace = miller_rabin(n)
        if passed:
            return n, trace, rejected
        rejected.append((n, "не пройшло тест Міллера–Рабіна"))

def main():
    p, trace, rejected = generate_prime()
    s, d, a, values = trace
    print("Пошук простого числа")
    print(f"Кількість перевірених кандидатів: {len(rejected) + 1}")
    print(f"Кількість відхилених кандидатів: {len(rejected)}")
    print("\nПерші п'ять відхилених кандидатів:")
    for n, reason in rejected[:5]:
        print(f"{n} — {reason}")
    print(f"\nЗнайдене число p = {p}")
    print(f"Довжина: {p.bit_length()} біт")
    print("Кількість раундів тесту Міллера–Рабіна: 32")
    print("\nПроміжні результати першого раунду:")
    print(f"p - 1 = 2^{s} * {d}")
    print(f"s = {s}")
    print(f"d = {d}")
    print(f"Основа a = {a}")
    print(f"x_0 = a^d mod p = {values[0]}")
    for r, x in enumerate(values[1:], 1):
        print(f"x_{r} = x_{r - 1}^2 mod p = {x}")
    if values[0] == 1:
        print("x_0 = 1 — раунд пройдено.")
    else:
        print(f"x_{len(values) - 1} = p - 1 — раунд пройдено.")
    print("\nУсі 32 раунди пройдено: число є ймовірно простим.")
    print("Верхня межа ймовірності проходження тесту складеним числом:")
    print(f"4^(-32) = {4 ** (-32):.6e}")

if __name__ == "__main__":
    main()
