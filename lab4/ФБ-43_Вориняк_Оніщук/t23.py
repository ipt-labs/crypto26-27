import random
from t1 import trial_division_test, miller_rabin_test, modular_exponentiation

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise Exception("Оберненого елемента не існує. e та phi не взаємно прості!")
    return (x % phi + phi) % phi

def generate_prime_for_report(bits=256, name="p"):
    failed_candidates = []
    while True:
        candidate = random.getrandbits(bits) | (1 << bits - 1) | 1
        if not trial_division_test(candidate):
            if len(failed_candidates) < 3:
                failed_candidates.append(candidate)
            continue
        if miller_rabin_test(candidate, k=20, debug=False):
            print(f"\n[+] Згенеровано просте число {name} = {candidate}")
            print(f"[-] Приклади кандидатів, що не пройшли перевірку на простоту:")
            for i, failed in enumerate(failed_candidates):
                print(f"    Кандидат {i+1}: {failed}")
            return candidate
        else:
            if len(failed_candidates) < 3:
                failed_candidates.append(candidate)

def run_debug_for_prime(p):
    print(f"\n[*] Дебаг Міллера-Рабіна для підтвердженого простого числа:\n{p}")
    miller_rabin_test(p, k=1, debug=True)

def GenerateKeyPair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    gcd, _, _ = extended_gcd(e, phi)
    while gcd != 1:
        e += 2
        gcd, _, _ = extended_gcd(e, phi)
    d = mod_inverse(e, phi)
    return {"public": (n, e), "private": (d, p, q)}

if __name__ == "__main__":
    print("="*43)
    print("Завдання 2. ГЕНЕРАЦІЯ ПРОСТИХ ЧИСЕЛ ТА ПАРАМЕТРІВ")
    print("="*43)
    # Генеруємо p, q для Абонента А
    p = generate_prime_for_report(bits=256, name="p")
    run_debug_for_prime(p)
    q = generate_prime_for_report(bits=256, name="q")
    
    # Генеруємо p1, q1 для Абонента B
    p1 = generate_prime_for_report(bits=256, name="p1")
    q1 = generate_prime_for_report(bits=256, name="q1")
    
    n_A = p * q
    n_B = p1 * q1
    
    if n_A > n_B:
        print("\n[!] n_A > n_B. Міняємо ключі місцями для коректної роботи протоколу розсилання ключів.")
        p, p1 = p1, p
        q, q1 = q1, q
        n_A, n_B = n_B, n_A

    print("\n" + "="*43)
    print("Завдання 3. ГЕНЕРАЦІЯ КЛЮЧІВ")
    print("="*43)
    keys_A = GenerateKeyPair(p, q)
    keys_B = GenerateKeyPair(p1, q1)
    print("\n[АБОНЕНТ A]")
    print(f"Відкритий ключ (e, n):\n  e = {keys_A['public'][1]}\n  n = {keys_A['public'][0]}")
    print(f"Секретний ключ d:\n  d = {keys_A['private'][0]}")
    print("\n[АБОНЕНТ B]")
    print(f"Відкритий ключ (e1, n1):\n  e1 = {keys_B['public'][1]}\n  n1 = {keys_B['public'][0]}")
    print(f"Секретний ключ d1:\n  d1 = {keys_B['private'][0]}")
    
    print("\n" + "="*43)
    print("ПЕРЕВІРКА СПІВВІДНОШЕНЬ")
    print("="*43)    
    phi_A = (keys_A['private'][1] - 1) * (keys_A['private'][2] - 1)
    e_A = keys_A['public'][1]
    d_A = keys_A['private'][0]
    
    check_val = (e_A * d_A) % phi_A
    print(f"Перевірка (e * d) mod phi == 1 для Абонента А: {check_val}")
    if check_val == 1:
        print("[+] Співвідношення виконується коректно! RSA математика налаштована правильно.")
    else:
        print("[-] ПОМИЛКА: Співвідношення не виконується!")