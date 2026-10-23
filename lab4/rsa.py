import random
from prime import power, gcd, inv


def gen_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 2 ** 16 + 1
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi - 1)
    d = inv(e, phi)
    return (n, e), (d, p, q)


def encrypt(m, pub):
    n, e = pub
    return power(m, e, n)


def decrypt(c, priv):
    d, p, q = priv
    return power(c, d, p * q)


def sign(m, priv):
    d, p, q = priv
    return power(m, d, p * q)


def verify(m, s, pub):
    n, e = pub
    return power(s, e, n) == m


def send_key(k, priv_a, pub_b):
    k1 = encrypt(k, pub_b)
    s = sign(k, priv_a)
    s1 = encrypt(s, pub_b)
    return k1, s1


def receive_key(k1, s1, priv_b, pub_a):
    k = decrypt(k1, priv_b)
    s = decrypt(s1, priv_b)
    if not verify(k, s, pub_a):
        return None
    return k
