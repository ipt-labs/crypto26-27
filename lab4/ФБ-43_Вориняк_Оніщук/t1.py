import random

SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
    233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
    283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
    353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
    419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
    467, 479, 487, 491, 499, 503, 509, 521, 523, 541
]

def modular_exponentiation(x, alpha, m):
    binary_alpha = bin(alpha)[2:] 
    y = 1
    for bit in binary_alpha:
        y = (y * y) % m
        if bit == '1':
            y = (y * x) % m
    return y

def trial_division_test(n):
    for p in SMALL_PRIMES:
        if n % p == 0:
            return False
    return True

def miller_rabin_test(p, k=20, debug=False):
    s = 0
    d = p - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    if debug:
        print(f"[*] Дебаг Міллера-Рабіна для числа p = {p}")
        print(f"[-] Розклад p-1: d = {d}, s = {s}")

    for i in range(k):
        x = random.randrange(2, p - 1)
        if debug and i == 0:
            print(f"[-] Обрано основу x = {x}")
        x_r = modular_exponentiation(x, d, p)
        if debug and i == 0:
            print(f"[-] x_0 = (x^d mod p) = {x_r}")
            
        if x_r == 1 or x_r == p - 1:
            if debug and i == 0:
                print("[+] Основа пройшла перевірку: x^d mod p == 1 або p-1")
            continue
            
        is_composite = True
        for r in range(1, s):
            x_r = modular_exponentiation(x_r, 2, p)
            if debug and i == 0:
                print(f"[-] x_{r} = (x_{r-1}^2 mod p) = {x_r}")
                
            if x_r == p - 1:
                is_composite = False
                if debug and i == 0:
                    print(f"[+] Основа пройшла перевірку на кроці r = {r} отримали p-1")
                break
                
        if is_composite:
            if debug and i == 0:
                print("[-] Число складене.")
            return False
    return True

def generate_prime_number(bits=256, debug_first=False):
    print(f"[*] Починаємо генерацію {bits}-бітного простого числа...")
    attempts = 0
    
    while True:
        attempts += 1
        candidate = random.getrandbits(bits)
        candidate |= (1 << bits - 1) | 1
        
        if not trial_division_test(candidate):
            continue
        if miller_rabin_test(candidate, k=20, debug=False):
            print(f"[+] Знайдено просте число за {attempts} спроб")
            if debug_first:
                print(f"\n[*] Дебаг Міллера-Рабіна для підтвердженого простого числа:\n{candidate}")
                miller_rabin_test(candidate, k=1, debug=True)
            return candidate

if __name__ == "__main__":
    p = generate_prime_number(bits=256, debug_first=True)
    print(f"\n[РЕЗУЛЬТАТ] Згенероване число p:\n{p}")