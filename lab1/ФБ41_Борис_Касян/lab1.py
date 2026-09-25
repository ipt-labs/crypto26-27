from pathlib import Path
import re
import math
from collections import Counter
import random

ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

def normalize_text(text):
    text = text.lower()
    text = "".join(
        symbol if symbol in ALPHABET else " "
        for symbol in text
    )
    text = re.sub(r" +", " ", text)
    return text.strip()

def calculate_h1(text):
    counts = Counter(text)
    total = len(text)
    h1 = 0

    # Обчислення ймовірності кожного символу та ентропії
    for count in counts.values():
        p = count / total
        h1 -= p * math.log2(p)
    return counts, h1


# Обчислення частот біграм та H2
def calculate_h2(text, step):
    bigrams = []

    # Формування біграм зі зміщенням на 1 або 2 символи
    for i in range(0, len(text) - 1, step):
        bigrams.append(text[i:i + 2])
    counts = Counter(bigrams)
    total = len(bigrams)
    h = 0

    # Обчислення ентропії біграм
    for count in counts.values():
        p = count / total
        h -= p * math.log2(p)

    # Перерахунок ентропії біграми на один символ
    h2 = h / 2
    return counts, h2, total


# Зчитування початкового тексту з файлу
folder = Path(__file__).resolve().parent
input_file = folder / "harry_potter_4.txt"
text = input_file.read_text(encoding="utf-8")
print(
    "Розмір файлу:",
    round(input_file.stat().st_size / 1024 / 1024, 2),
    "МБ"
)
print("Кількість символів:", len(text))

text_with_spaces = normalize_text(text)
text_without_spaces = text_with_spaces.replace(" ", "")

# Збереження нормалізованого тексту з пробілами
(folder / "text_normalized.txt").write_text(
    text_with_spaces,
    encoding="utf-8"
)
# без пробілів
(folder / "text_no_spaces.txt").write_text(
    text_without_spaces,
    encoding="utf-8"
)
print("\nНормалізацію завершено.")
print("Початковий текст:", len(text), "символів")
print("Нормалізований текст:", len(text_with_spaces), "символів")
print("Текст без пробілів:", len(text_without_spaces), "символів")
print("\nПерші 400 символів:")
print(text_with_spaces[:400])


# Обчислення H1 для тексту з пробілами
counts_spaces, h1_spaces = calculate_h1(text_with_spaces)
print("\n--- Текст з пробілами ---")
print("H1 =", round(h1_spaces, 5))
# Виведення п'яти найчастіших символів у тексті з пробілами
print("Топ-5 символів:")
for symbol, count in counts_spaces.most_common(5):
    p = count / len(text_with_spaces)
    if symbol == " ":
        symbol = "пробіл"
    print(symbol, "-", round(p, 6))


# Обчислення H1 для тексту без пробілів
counts_no_spaces, h1_no_spaces = calculate_h1(text_without_spaces)
print("\n--- Текст без пробілів ---")
print("H1 =", round(h1_no_spaces, 5))
# Виведення п'яти найчастіших символів у тексті без пробілів
print("Топ-5 символів:")
for symbol, count in counts_no_spaces.most_common(5):
    p = count / len(text_without_spaces)
    print(symbol, "-", round(p, 6))


# Обчислення H2 для тексту з пробілами та біграм, що перетинаються
bigram_spaces_overlap, h2_spaces_overlap, total1 = calculate_h2(
    text_with_spaces, 1
)
# Обчислення H2 для тексту з пробілами та біграм, що не перетинаються
bigram_spaces_no_overlap, h2_spaces_no_overlap, total2 = calculate_h2(
    text_with_spaces, 2
)

# Виведення значень H2 для тексту з пробілами
print("\n--- H2 для тексту з пробілами ---")
print("З перетином =", round(h2_spaces_overlap, 5))
print("Без перетину =", round(h2_spaces_no_overlap, 5))

# Виведення п'яти найчастіших біграм, що перетинаються
print("Топ-5 біграм з перетином:")
for bigram, count in bigram_spaces_overlap.most_common(5):
    print(
        bigram.replace(" ", "_"),
        "-",
        round(count / total1, 6)
    )
# Виведення п'яти найчастіших біграм, що не перетинаються
print("Топ-5 біграм без перетину:")
for bigram, count in bigram_spaces_no_overlap.most_common(5):
    print(
        bigram.replace(" ", "_"),
        "-",
        round(count / total2, 6)
    )


# Обчислення H2 для тексту без пробілів та біграм, що перетинаються
bigram_no_spaces_overlap, h2_no_spaces_overlap, total3 = calculate_h2(
    text_without_spaces, 1
)
# Обчислення H2 для тексту без пробілів та біграм, що не перетинаються
bigram_no_spaces_no_overlap, h2_no_spaces_no_overlap, total4 = calculate_h2(
    text_without_spaces, 2
)

# Виведення значень H2 для тексту без пробілів
print("\n--- H2 для тексту без пробілів ---")
print("З перетином =", round(h2_no_spaces_overlap, 5))
print("Без перетину =", round(h2_no_spaces_no_overlap, 5))

# Виведення п'яти найчастіших біграм, що перетинаються
print("Топ-5 біграм з перетином:")
for bigram, count in bigram_no_spaces_overlap.most_common(5):
    print(
        bigram,
        "-",
        round(count / total3, 6)
    )

# Виведення п'яти найчастіших біграм, що не перетинаються
print("Топ-5 біграм без перетину:")

for bigram, count in bigram_no_spaces_no_overlap.most_common(5):
    print(
        bigram,
        "-",
        round(count / total4, 6)
    )

# Експеримент А, Б, В
length = 50000

# Послідовність А — фрагмент природного російськомовного тексту
sequence_a = text_without_spaces[:length]
# Послідовність Б — повторення одного символу
sequence_b = "а" * length
# Послідовність В — випадкова рівноймовірна послідовність
random.seed(42)
sequence_v = ""
for i in range(length):
    sequence_v += random.choice(ALPHABET)


# Обчислення H1 для послідовностей А, Б, В
counts_a, h1_a = calculate_h1(sequence_a)
counts_b, h1_b = calculate_h1(sequence_b)
counts_v, h1_v = calculate_h1(sequence_v)

# Виведення результатів експерименту А, Б, В
print("\n--- Експеримент А, Б, В ---")
print("А — природний текст")
print("H1 =", round(h1_a, 5))
print("\nБ — повторення одного символу")
print("H1 =", round(h1_b, 5))
print("\nВ — випадкова рівноймовірна послідовність")
print("H1 =", round(h1_v, 5))


# Експеримент Г, Д
length_gd = 50000
half = length_gd // 2

# Послідовність Г — однакова кількість символів "а" і "б" у випадковому порядку
sequence_g_list = ["а"] * half + ["б"] * half
random.seed(123)
random.shuffle(sequence_g_list)
sequence_g = "".join(sequence_g_list)

# Послідовність Д — періодична структура "абабаб..."
sequence_d = "аб" * half


# Обчислення H1 для послідовностей Г і Д
counts_g, h1_g = calculate_h1(sequence_g)
counts_d, h1_d = calculate_h1(sequence_d)

# Обчислення H2 для біграм, що перетинаються
_, h2_g_overlap, _ = calculate_h2(sequence_g, 1)
_, h2_d_overlap, _ = calculate_h2(sequence_d, 1)
# Обчислення H2 для біграм, що не перетинаються
_, h2_g_no_overlap, _ = calculate_h2(sequence_g, 2)
_, h2_d_no_overlap, _ = calculate_h2(sequence_d, 2)


# Виведення результатів експерименту Г, Д
print("\n--- Експеримент Г, Д ---")
print("Г — випадковий порядок")
print("H1 =", round(h1_g, 5))
print("H2 з перетином =", round(h2_g_overlap, 5))
print("H2 без перетину =", round(h2_g_no_overlap, 5))

print("\nД — періодична послідовність")
print("H1 =", round(h1_d, 5))
print("H2 з перетином =", round(h2_d_overlap, 5))
print("H2 без перетину =", round(h2_d_no_overlap, 5))
