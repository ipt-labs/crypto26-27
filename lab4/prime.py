import random

small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def power(x, a, m):
    y = 1
    for bit in bin(a)[2:]:
        y = y * y % m
        if bit == '1':
            y = y * x % m
    return y


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def inv(a, m):
    r0, r1 = a, m
    s0, s1 = 1, 0
    while r1:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if r0 != 1:
        raise ValueError("оберненого немає")
    return s0 % m


def trial(n):
    for p in small:
        if n % p == 0:
            return n == p
    return True


def miller_rabin(n, k=20, log=False):
    if n < 2:
        return False
    if n in small:
        return True
    if not trial(n):
        return False

    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    if log:
        print(f"n = {n}\nn-1 = d * 2^s, s = {s}, d = {d}")

    for i in range(k):
        x = random.randrange(2, n - 1)
        if gcd(x, n) != 1:
            if log:
                print(f"основа {x}: gcd != 1, складене")
            return False

        y = power(x, d, n)
        if log:
            print(f"\nоснова x = {x}\nx^d mod n = {y}")
        if y == 1 or y == n - 1:
            if log:
                print("-> сильно псевдопросте за цією основою")
            continue

        ok = False
        for r in range(1, s):
            y = y * y % n
            if log:
                print(f"r = {r}: {y}")
            if y == n - 1:
                ok = True
                break
            if y == 1:
                break
        if not ok:
            if log:
                print("-> не сильно псевдопросте, складене")
            return False
        if log:
            print("-> сильно псевдопросте за цією основою")
    return True


def gen_prime(bits, bad=None, log=False):
    while True:
        n = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if miller_rabin(n, log=log):
            return n
        if bad is not None:
            bad.append(n)
