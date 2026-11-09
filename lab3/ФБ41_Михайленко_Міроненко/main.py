import math
from collections import Counter
from itertools import permutations

ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя"
M = 31
M2 = M ** 2

def char_to_int(c): return ALPHABET.index(c)
def int_to_char(i): return ALPHABET[i]

def bigram_to_int(b):
    return char_to_int(b[0]) * M + char_to_int(b[1])

def int_to_bigram(val):
    return int_to_char(val // M) + int_to_char(val % M)

def ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = ext_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    g, x, y = ext_gcd(a, m)
    if g != 1: return None
    return x % m

def solve_linear_congruence(a, b, m):
    g, u, v = ext_gcd(a, m)
    if b % g != 0:
        return []
    x0 = (u * (b // g)) % m
    return [(x0 + i * (m // g)) % m for i in range(g)]

def check_meaningful(text):
    forbidden = ['ьь', 'ыы', 'ьы', 'йь', 'эь', 'аь', 'оь', 'уь', 'еь', 'юь', 'яь', 'иь', 'щщ']
    for fb in forbidden:
        if fb in text:
            return False
    
    freq = Counter(text)
    top_chars = sum(freq[c] for c in 'оеаинтс') / len(text)
    if top_chars < 0.4:
        return False
        
    return True

def main():
    filename = "07 (utf8).txt"
    with open(filename, "r", encoding="utf-8") as f:
        ciphertext = f.read().replace('\n', '').strip()
        
    cipher_bigrams = [ciphertext[i:i+2] for i in range(0, len(ciphertext)-1, 2)]
    bg_counts = Counter(cipher_bigrams)
    top5_cipher = [bg for bg, cnt in bg_counts.most_common(5)]
    print(f"Топ-5 біграм шифртексту: {top5_cipher}")
    
    top5_plain = ['ст', 'но', 'то', 'на', 'ен']
    
    candidates = set()
    
    for p1, p2 in permutations(top5_plain, 2):
        for c1, c2 in permutations(top5_cipher, 2):
            X1, X2 = bigram_to_int(p1), bigram_to_int(p2)
            Y1, Y2 = bigram_to_int(c1), bigram_to_int(c2)
            
            dY = (Y1 - Y2) % M2
            dX = (X1 - X2) % M2
            
            possible_a = solve_linear_congruence(dX, dY, M2)
            
            for a in possible_a:
                if math.gcd(a, M) == 1:
                    b = (Y1 - a * X1) % M2
                    candidates.add((a, b))
                    
    print(f"Сформовано кандидатів на ключ: {len(candidates)}")
    
    for a, b in candidates:
        a_inv = mod_inverse(a, M2)
        if not a_inv: continue
        
        plaintext = ""
        for cb in cipher_bigrams:
            Y = bigram_to_int(cb)
            X = (a_inv * (Y - b)) % M2
            plaintext += int_to_bigram(X)
            
        if check_meaningful(plaintext):
            print(f"\n[+] УСПІХ! Ключ знайдено: a = {a}, b = {b}")
            print(f"Фрагмент тексту: {plaintext[:150]}...")
            with open("decrypted_07.txt", "w", encoding="utf-8") as out:
                out.write(plaintext)
            break

if __name__ == "__main__":
    main()