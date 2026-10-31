from Task1 import generate_prime

def generate_subscriber_primes(bits=256):
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)
    return p, q

def generate_both_pairs(bits=256):
    p, q = generate_subscriber_primes(bits)
    p1, q1 = generate_subscriber_primes(bits)

    n = p * q
    n1 = p1 * q1

    if n > n1:
        p, q, p1, q1 = p1, q1, p, q
        n, n1 = n1, n

    return (p, q, n), (p1, q1, n1)

if __name__ == "__main__":
    (p, q, n), (p1, q1, n1) = generate_both_pairs(bits=256)

    print("Subscriber A:")
    print(f"p={p}")
    print(f"q={q}")
    print(f"n={n}")
    print(f"Bits(n)={n.bit_length()}")

    print("\nSubscriber B:")
    print(f"p1={p1}")
    print(f"q1={q1}")
    print(f"n1={n1}")
    print(f"Bits(n1)={n1.bit_length()}")

    print("\nVerification:")
    print(f"Condition n <= n1: {n <= n1}")
    print(f"Difference (n1 - n) >= 0: {n1 - n >= 0}") 