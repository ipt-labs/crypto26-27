def extended_gcd(a, b):
    u0, u1 = 1, 0
    v0, v1 = 0, 1
    while b != 0:
        q = a // b
        a, b = b, a - q * b
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return a, u0, v0

def mod_inverse(a, n):
    d, u, _ = extended_gcd(a % n, n)
    if d != 1:
        return None
    return u % n

def solve_congruence(a, b, n):
    a = a % n
    b = b % n
    d, u, _ = extended_gcd(a, n)
    if b % d != 0:
        return []
    n1 = n // d
    x0 = (u * (b // d)) % n1
    return [x0 + k * n1 for k in range(d)]
    
if __name__ == "__main__":
    print(mod_inverse(3, 961))
    print(3 * mod_inverse(3, 961) % 961)
    print(mod_inverse(31, 961))

    print(solve_congruence(3, 63, 961))
    print(solve_congruence(2, 4, 8))
    print(solve_congruence(4, 3, 8))
    print(solve_congruence(6, 4, 8))