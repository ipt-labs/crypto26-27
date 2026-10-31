import secrets
from Task1 import mod_pow
from Task2 import generate_both_pairs
from Task3 import GenerateKeyPair
from Task4 import Encrypt, Decrypt, Sign, Verify

def SendKey(k, e1, n1, d, n):
    if not (0 < k < n):
        raise ValueError("Error1")
    if n > n1:
        raise ValueError("Error2")

    S = Sign(k, d, n)
    k1 = Encrypt(k, e1, n1)
    S1 = Encrypt(S, e1, n1)
    return k1, S1

def ReceiveKey(k1, S1, d1, n1, e, n):
    k = Decrypt(k1, d1, n1)
    S = Decrypt(S1, d1, n1)
    is_valid = Verify(k, S, e, n)
    return k, is_valid

if __name__ == "__main__":
    (p, q, n), (p1, q1, n1) = generate_both_pairs(bits=256)
    (e, n), (d, p, q) = GenerateKeyPair(p, q)
    (e1, n1), (d1, p1, q1) = GenerateKeyPair(p1, q1)

    k = secrets.randbelow(n - 2) + 2
    print(f"Generated secret session key k:")
    print(f"k = {k}")

    print("\nSender A: SendKey ")
    k1, S1 = SendKey(k, e1, n1, d, n)
    print(f"Encrypted key k1: {k1}")
    print(f"Encrypted signature S1: {S1}")

    print("\nReceiver B: ReceiveKey ")
    received_k, is_valid = ReceiveKey(k1, S1, d1, n1, e, n)
    print(f"Decrypted key k: {received_k}")
    print(f"Signature valid: {is_valid}")
    print(f"Key match (received_k == k): {received_k == k}")

    print("\nChannel Tampering Simulation ")
    tampered_k1 = (k1 + 1) % n1
    tampered_received_k, tampered_is_valid = ReceiveKey(tampered_k1, S1, d1, n1, e, n)
    print(f"Tampered transmission signature valid: {tampered_is_valid}")