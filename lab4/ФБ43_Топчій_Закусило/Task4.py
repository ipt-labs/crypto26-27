import secrets
from Task1 import mod_pow
from Task2 import generate_both_pairs
from Task3 import GenerateKeyPair

def Encrypt(message, e, n):
    if not (0 <= message < n):
        raise ValueError("Message out of bounds: must be 0 <= message < n")
    return mod_pow(message, e, n)

def Decrypt(ciphertext, d, n):
    if not (0 <= ciphertext < n):
        raise ValueError("Ciphertext out of bounds: must be 0 <= ciphertext < n")
    return mod_pow(ciphertext, d, n)

def Sign(message, d, n):
    if not (0 <= message < n):
        raise ValueError("Message out of bounds: must be 0 <= message < n")
    return mod_pow(message, d, n)

def Verify(message, signature, e, n):
    if not (0 <= signature < n):
        return False
    return mod_pow(signature, e, n) == message

if __name__ == "__main__":
    (p, q, n), (p1, q1, n1) = generate_both_pairs(bits=256)
    (e, n), (d, p, q) = GenerateKeyPair(p, q)
    (e1, n1), (d1, p1, q1) = GenerateKeyPair(p1, q1)

    M = secrets.randbelow(n - 1) + 1
    print(f"Original message M: {M}")

    print("\nSubscriber A Operations ")
    C_A = Encrypt(M, e, n)
    M_dec_A = Decrypt(C_A, d, n)
    print(f"Ciphertext C_A: {C_A}")
    print(f"Decryption success for A: {M_dec_A == M}")

    S_A = Sign(M, d, n)
    verify_A = Verify(M, S_A, e, n)
    print(f"Signature S_A: {S_A}")
    print(f"Signature verification for A: {verify_A}")

    print("\nSubscriber B Operations ")
    C_B = Encrypt(M, e1, n1)
    M_dec_B = Decrypt(C_B, d1, n1)
    print(f"Ciphertext C_B: {C_B}")
    print(f"Decryption success for B: {M_dec_B == M}")

    S_B = Sign(M, d1, n1)
    verify_B = Verify(M, S_B, e1, n1)
    print(f"Signature S_B: {S_B}")
    print(f"Signature verification for B: {verify_B}")

    print("\nTampering Check ")
    tampered_M = M + 1
    tampered_verify = Verify(tampered_M, S_A, e, n)
    print(f"Verification of tampered message: {tampered_verify}")