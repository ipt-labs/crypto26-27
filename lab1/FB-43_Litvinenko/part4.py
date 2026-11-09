import random as r
from math import log2

# Алфавіт
ru = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж',
    'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
    'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц',
    'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'
]

# Вибираємо 3 різні символи
symbols = r.sample(ru, 3)

# Створюємо періодичну послідовність Д
ln = 9999
D = ''.join(symbols[i % 3] for i in range(ln))

# Створюємо Г з тих самих символів у випадковому порядку
G_list = list(D)
r.shuffle(G_list)
G = ''.join(G_list)


# Функція для обчислення H1
def calculate_H1(text):
    counts = {}

    for char in text:
        counts[char] = counts.get(char, 0) + 1

    total = len(text)
    H1 = 0

    for count in counts.values():
        p = count / total
        H1 -= p * log2(p)

    return H1


# Функція для обчислення H2
# step=1 — біграми перетинаються
# step=2 — біграми не перетинаються
def calculate_H2(text, step):
    bigrams = {}

    for i in range(0, len(text) - 1, step):
        bigram = text[i:i + 2]
        bigrams[bigram] = bigrams.get(bigram, 0) + 1

    total = sum(bigrams.values())
    H2 = 0

    for count in bigrams.values():
        p = count / total
        H2 -= p * log2(p)

    return H2


# Обчислення ентропії
H1_G = calculate_H1(G)
H1_D = calculate_H1(D)

H2_G_p = calculate_H2(G, 1)
H2_D_p = calculate_H2(D, 1)

H2_G_np = calculate_H2(G, 2)
H2_D_np = calculate_H2(D, 2)


# Виведення результатів
print("ПУНКТ 4. ДОСЛІДЖЕННЯ ЗАЛЕЖНОСТЕЙ МІЖ СИМВОЛАМИ")
print("-" * 50)

print("Використані символи:", symbols)
print("Довжина G:", len(G))
print("Довжина D:", len(D))

print("\nЕнтропія H1:")
print("H1(G) — випадкова послідовність:", H1_G)
print("H1(D) — періодична послідовність:", H1_D)

print("\nH2 для біграм, що перетинаються:")
print("H2(G):", H2_G_p)
print("H2(D):", H2_D_p)

print("\nH2 для біграм, що не перетинаються:")
print("H2(G):", H2_G_np)
print("H2(D):", H2_D_np)
