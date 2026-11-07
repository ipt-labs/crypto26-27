import sys
from gen_prime_rand import *

def generate_strong_prime(start, end):
    p_prime = search_in_interval(start, end)

    print(f"Знайдено просте число p' = {p_prime} у діапазоні [{start.bit_length()}, {end.bit_length()}] біт.")
    
    i = 1
    while True:
        p = 2 * i * p_prime + 1
        if Miller_Rabin(p):
            print(f"Знайдено стійке просте число p = {p} (2 * {i} * p' + 1).")
            return p
        print(f"p = 2 * {i} * p' + 1 = {p} не є простим. Продовжуємо пошук...")
        i += 1

def propper_rsa_primes(size):

    start = 2 ** (size - 2)
    end = 2 ** (size - 1) - 1
    
    p = generate_strong_prime(start, end)
    
    while True:
        q = generate_strong_prime(start, end)
        if p != q:
            break
            
    return p, q

def generate_rsa_primes(size):
    p_A, q_A = propper_rsa_primes(size)

    p_B, q_B = propper_rsa_primes(size)

    if p_A * q_A < p_B * q_B:
        return (p_A, q_A), (p_B,  q_B)
    else:
        return (p_B, q_B), (p_A, q_A)

if __name__ == "__main__":
    size = int(sys.argv[1])
    key_pair = generate_rsa_primes(size)
    print(key_pair)
