def egcd(a, b):
    u0, u1, v0, v1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return a, u0, v0


def inverse(a, n):
    d, u, _ = egcd(a % n, n)
    return u % n if d == 1 else None


def solve(a, b, n):
    a, b = a % n, b % n
    d = egcd(a, n)[0]
    if b % d:
        return []
    n1 = n // d
    x0 = b // d * inverse(a // d, n1) % n1
    return [x0 + k * n1 for k in range(d)]


if __name__ == "__main__":
    print("17^(-1) mod 961 =", inverse(17, 961))
    print("-155x = 248 (mod 961):", solve(-155, 248, 961))
    print("-155x = 250 (mod 961):", solve(-155, 250, 961))
