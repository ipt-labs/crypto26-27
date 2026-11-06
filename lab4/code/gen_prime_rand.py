import random
import math
import sys

SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)

def search_in_interval(start, end, verbose=False):
    is_prime = False
    while not is_prime:
        if start > end:
            start, end = end, start

        num = random.randint(start, end)
        if Miller_Rabin(num, verbose=verbose):
            is_prime = True

    return num

def Miller_Rabin(n, k=10, verbose=False):
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if n == p:
            return True
        if n % p == 0:
            return False

    s, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    if verbose:
        print(f"\nТестуємо {n} на простоту з {k} ітераціями.")
        print(f"Розкладаємо {n-1} як 2^{s} * {d}")

    for i in range(k):
        a = random.randint(2, n - 2)
        if verbose:
            print(f"\n--- Ітерація {i+1} ---")
            print(f"Випадкова основа a: {a}")

        if math.gcd(a, n) != 1:
            if verbose:
                print(f"gcd({a}, {n}) != 1, отже {n} є складеним числом.")
            return False

        x = pow(a, d, n)
        if verbose:
            print(f"Обчислюємо {a}^{d} mod {n} = {x}")
            
        if x == 1 or x == n - 1:
            if verbose:
                print(f"{n} може бути простим (x = {x}). Переходимо до наступної ітерації.")
            continue
            
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if verbose:
                print(f"Обчислюємо x^2 mod {n} = {x}")
            if x == n - 1:
                if verbose:
                    print(f"Знайдено -1 (x = {x}). Переходимо до наступної ітерації.")
                break
            if x == 1:
                if verbose:
                    print(f"Знайдено 1 у послідовності квадратів. {n} є складеним числом.")
                return False    
                
        else:
            if verbose:
                print(f"Не знайдено -1 у послідовності квадратів. {n} є складеним числом.")
            return False
            
    if verbose:
        print(f"\nВсі {k} ітерацій пройдено. {n} з високою ймовірністю є простим.")
    return True


if __name__ == "__main__":

    args = [a for a in sys.argv[1:] if a != "verbose"]
    verbose = "verbose" in sys.argv[1:]

    if len(args) == 3 and args[0] == "int":
        start = int(args[1])
        end = int(args[2])
    elif len(args) == 2 and args[0] == "size":
        size = int(args[1])
        start = 2 ** (size - 1)
        end = 2 ** size - 1
    else:
        print("Використання:\n"
              "  python gen_prime_rand.py size <кількість_біт> [verbose]\n"
              "  python gen_prime_rand.py int <початок> <кінець> [verbose]")
        sys.exit(1)

    prime_number = search_in_interval(start, end, verbose)
    print(prime_number)
