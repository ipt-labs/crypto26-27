import random

SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
                127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181,
                191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251]


def power_mod(x, alpha, m):
    y = 1
    for bit in bin(alpha)[2:]:
        y = y * y % m
        if bit == '1':
            y = y * x % m
    return y


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def trial_division(n):
    for p in SMALL_PRIMES:
        if n % p == 0:
            return p
    return None


def miller_rabin(n, a):
    if gcd(a, n) != 1:
        return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = power_mod(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def miller_rabin_trace(n, a):
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    steps = []
    x = power_mod(a, d, n)
    steps.append(('x = a^d mod n', x))
    if x == 1 or x == n - 1:
        return d, s, steps, True
    for r in range(1, s):
        x = x * x % n
        steps.append((f'x = x^2 mod n  (r = {r})', x))
        if x == n - 1:
            return d, s, steps, True
        if x == 1:
            return d, s, steps, False
    return d, s, steps, False


def is_prime(n, rounds=20):
    if n < 2:
        return False
    if n in SMALL_PRIMES:
        return True
    if trial_division(n) is not None:
        return False
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        if not miller_rabin(n, a):
            return False
    return True


def gen_prime(bits, rounds=20, log=None):
    while True:
        n = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        div = trial_division(n)
        if div is not None:
            if log is not None:
                log.append((n, f'пробні ділення: кратне {div}'))
            continue
        for i in range(rounds):
            a = random.randrange(2, n - 1)
            if not miller_rabin(n, a):
                if log is not None:
                    log.append((n, f'Міллер-Рабін: складене, основа a = {a} '
                                   f'(раунд {i + 1})'))
                break
        else:
            return n


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def inverse(a, m):
    g, x, _ = egcd(a % m, m)
    if g != 1:
        return None
    return x % m


def GenerateKeyPair(bits=256, e=65537, log=None, p=None, q=None):
    given = p is not None and q is not None
    while True:
        pp = p if p is not None else gen_prime(bits, log=log)
        qq = q if q is not None else gen_prime(bits, log=log)
        if pp == qq:
            if given:
                raise ValueError('p і q повинні бути різними')
            continue
        phi = (pp - 1) * (qq - 1)
        if phi % e == 0:
            if given:
                raise ValueError('e не взаємно просте з phi(n)')
            continue
        d = inverse(e, phi)
        return (e, pp * qq), (d, pp, qq)


def Encrypt(message, public_key):
    e, n = public_key
    return power_mod(message, e, n)


def Decrypt(ciphertext, private_key):
    d, p, q = private_key
    return power_mod(ciphertext, d, p * q)


def Sign(message, private_key):
    d, p, q = private_key
    return power_mod(message, d, p * q)


def Verify(message, signature, public_key):
    e, n = public_key
    return power_mod(signature, e, n) == message % n


def SendKey(k, sender_private, receiver_public):
    d, p, q = sender_private
    n = p * q
    e1, n1 = receiver_public
    if not 0 < k < n:
        raise ValueError(f'порушено умову 0 < k < n: k = {k}, n = {n}')
    if n1 < n:
        raise ValueError(f'порушено умову n <= n1: n = {n}, n1 = {n1}')
    S = power_mod(k, d, n)
    k1 = power_mod(k, e1, n1)
    S1 = power_mod(S, e1, n1)
    return k1, S1


def ReceiveKey(k1, S1, receiver_private, sender_public):
    d1, p1, q1 = receiver_private
    n1 = p1 * q1
    e, n = sender_public
    if n1 < n:
        raise ValueError(f'порушено умову n <= n1: n = {n}, n1 = {n1}')
    k = power_mod(k1, d1, n1)
    S = power_mod(S1, d1, n1)
    if power_mod(S, e, n) != k:
        return None, k, S
    return k, k, S