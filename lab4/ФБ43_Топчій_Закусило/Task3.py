from Task1 import gcd, mod_pow
from Task2 import generate_both_pairs

def extended_gcd(a, b):
    u0, u1 = 1, 0
    v0, v1 = 0, 1
    while b != 0:
        q = a // b
        a, b = b, a - q * b
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return a, u0, v0

def mod_inverse(a, m):
    g, u, _ = extended_gcd(a % m, m)
    if g != 1:
        return None
    return u % m

def GenerateKeyPair(p, q, e=65537):
    n = p * q
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        raise ValueError("Error")
    d = mod_inverse(e, phi)
    return (e, n), (d, p, q)

if __name__ == "__main__":
    (p, q, n), (p1, q1, n1) = generate_both_pairs(bits=256)

    pub_A, priv_A = GenerateKeyPair(p, q)
    pub_B, priv_B = GenerateKeyPair(p1, q1)

    e, n = pub_A
    d, p, q = priv_A
    phi = (p - 1) * (q - 1)

    e1, n1 = pub_B
    d1, p1, q1 = priv_B
    phi1 = (p1 - 1) * (q1 - 1)

    print("Subscriber A Keys:")
    print(f"Public Key (e, n):")
    print(f"e = {e}")
    print(f"n = {n}")
    print(f"Private Key d = {d}")
    print(f"phi(n) = {phi}")

    print("\nSubscriber B Keys:")
    print(f"Public Key (e1, n1):")
    print(f"e1 = {e1}")
    print(f"n1 = {n1}")
    print(f"Private Key d1 = {d1}")
    print(f"phi(n1) = {phi1}")

    print("\nVerification for Subscriber A:")
    print(f"1. gcd(e, phi(n)) == 1: {gcd(e, phi) == 1}")
    print(f"2. (e * d) mod phi(n) == 1: {(e * d) % phi == 1}")

    test_message = 12345678901234567890
    ciphertext = mod_pow(test_message, e, n)
    decrypted = mod_pow(ciphertext, d, n)
    print(f"3. Decryption test (m^e)^d mod n == m: {decrypted == test_message}")