from math import log2
import random
ru = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж',
    'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
    'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц',
    'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'
]
with open(r"C:\Users\Tuf\Desktop\3 Курс\Крипта\lab1\no_space", "r", encoding="utf-8") as file:
    no_space = file.read()

A = no_space
B = 'а' * len(A)
V = ''.join(random.choice(ru) for _ in range(len(A)))

def calculate_H1(text):
    counts = {}
    for char in text:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1
    total = len(text)
    H1 = 0
    for count in counts.values():
        p = count / total
        H1 -= p * log2(p)
    return H1

H1_A = calculate_H1(A)
H1_B = calculate_H1(B)
H1_V = calculate_H1(V)

print("\n" + "--" * 20)
print("ПУНКТ 3. ВПЛИВ РОЗПОДІЛУ СИМВОЛІВ")
print("--" * 20)
print("H1(Б) — один символ 'a' =", H1_B)
print("H1(A) — природний текст =", H1_A)
print("H1(В) — випадкова послідовність =", H1_V)