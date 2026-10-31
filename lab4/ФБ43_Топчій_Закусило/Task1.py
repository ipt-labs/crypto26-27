import secrets

SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
    157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
    239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
    421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
    509, 521, 523, 541
]

def mod_pow(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    return result

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def trial_division(n):
    for prime in SMALL_PRIMES:
        if n == prime:
            return True
        if n % prime == 0:
            return False
    return True

def miller_rabin(p, k=40, verbose=False):
    if p < 2:
        return False
    if p in (2, 3):
        return True
    if p % 2 == 0:
        return False

    d = p - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    if verbose:
        print(f"p - 1 = 2^{s} * {d}")

    for round_idx in range(k):
        x = secrets.randbelow(p - 3) + 2
        g = gcd(x, p)
        if g > 1:
            return False

        xr = mod_pow(x, d, p)

        if verbose and round_idx == 0:
            print(f"Base x: {x}")
            print(f"x^d mod p = {xr}")

        if xr == 1 or xr == p - 1:
            continue

        composite = True
        for r in range(1, s):
            xr = mod_pow(xr, 2, p)
            if verbose and round_idx == 0:
                print(f"x^(d * 2^{r}) mod p = {xr}")
            if xr == p - 1:
                composite = False
                break
            if xr == 1:
                return False

        if composite:
            return False

    return True

def is_prime(n, k=40, verbose=False):
    if not trial_division(n):
        return False
    return miller_rabin(n, k=k, verbose=verbose)

def generate_prime_candidate(bits):
    candidate = secrets.randbits(bits)
    candidate |= (1 << (bits - 1)) | 1
    return candidate

def generate_prime(bits=256, k=40, collect_rejected=False):
    rejected = []
    while True:
        candidate = generate_prime_candidate(bits)
        if not trial_division(candidate):
            if collect_rejected and len(rejected) < 5:
                rejected.append((candidate, "Failed trial division"))
            continue
        if not miller_rabin(candidate, k=k):
            if collect_rejected and len(rejected) < 5:
                rejected.append((candidate, "Failed Miller-Rabin"))
            continue
        if collect_rejected:
            return candidate, rejected
        return candidate

if __name__ == "__main__":
    prime, rejected = generate_prime(bits=256, collect_rejected=True)
    print(f"Generated 256-bit prime: {prime}")

    print("\nIntermediate Miller-Rabin test steps for this prime:")
    miller_rabin(prime, k=1, verbose=True)

    print("\nRejected candidates sample:")
    for cand, reason in rejected:
        print(f"{cand} - {reason}")