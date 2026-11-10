def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0

    d, x, y = extended_gcd(b, a % b)
    return d, y, x - (a // b) * y

def mod_inverse(a, n):
    d, x, _ = extended_gcd(a % n, n)
    if d != 1:
        return None
    return x % n


def solve_congruence(a, b, n):
    a %= n
    b %= n
    d, x, _ = extended_gcd(a, n)

    if b % d != 0:
        return []

    reduced_n = n // d
    x0 = (x * (b // d)) % reduced_n

    return [x0 + k * reduced_n for k in range(d)]

if __name__ == "__main__":
    print("ОБЕРНЕНІ ЕЛЕМЕНТИ")
    for a, n in [(5, 961), (31, 961)]:
        inverse = mod_inverse(a, n)
        print(f"a = {a}, n = {n}: обернений елемент = {inverse}")
        if inverse is not None:
            print(f"Перевірка: ({a} * {inverse}) mod {n} = "
                  f"{(a * inverse) % n}")

    print("\nЛІНІЙНІ ПОРІВНЯННЯ")
    examples = [
        (5, 10, 961),
        (31, 62, 961),
        (31, 10, 961),
    ]

    for a, b, n in examples:
        solutions = solve_congruence(a, b, n)
        print(f"\n{a}x ≡ {b} (mod {n})")
        print(f"Кількість розв'язків: {len(solutions)}")
        print(f"Розв'язки: {solutions}")
        if solutions:
            print("Перевірка всіх розв'язків:",
                  all((a * x - b) % n == 0 for x in solutions))
