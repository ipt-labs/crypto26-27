import re
from collections import Counter
from math import log2
from random import choice, shuffle

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя "
output_lines = []


def print_result(message):
    print(message)
    output_lines.append(message)


def calculate_entropy(counts, block_length=1):
    total = sum(counts.values())
    entropy = 0

    for count in counts.values():
        frequency = count / total
        entropy -= frequency * log2(frequency)

    return entropy / block_length


def print_top_five(counts):
    total = sum(counts.values())

    for item, count in counts.most_common(5):
        frequency = count / total
        print_result(f"{item!r}: кількість = {count}, частота = {frequency:.6f}")


# 1. Підготовка тексту
with open("original_text.txt", encoding="utf-8") as file:
    text = file.read()

text = text.lower()
text = text.replace("ё", "е")

text_with_spaces = re.sub(r"[^а-я]+", " ", text).strip()
text_without_spaces = text_with_spaces.replace(" ", "")

with open("text_with_spaces.txt", "w", encoding="utf-8") as file:
    file.write(text_with_spaces)

with open("text_without_spaces.txt", "w", encoding="utf-8") as file:
    file.write(text_without_spaces)


# 2. Розрахунок статистичних характеристик тексту
for name, prepared_text, alphabet_size in [
    ("З пробілами", text_with_spaces, 33),
    ("Без пробілів", text_without_spaces, 32),
]:
    h0 = log2(alphabet_size)
    print_result(f"\n{name}")
    print_result(f"Кількість символів: {len(prepared_text)}")

    symbol_counts = Counter(prepared_text)
    h1 = calculate_entropy(symbol_counts)

    print_result(f"H1 = {h1:.6f} біт/символ")
    r1 = 1 - h1 / h0
    print_result(f"Надлишковість за H1 = {r1:.2%}")
    print_result("П'ять найчастіших символів:")
    print_top_five(symbol_counts)

    for step in [1, 2]:
        mode = "з перетином" if step == 1 else "без перетину"
        bigram_counts = Counter()

        for i in range(0, len(prepared_text) - 1, step):
            bigram = prepared_text[i:i + 2]
            bigram_counts[bigram] += 1

        h2 = calculate_entropy(bigram_counts, block_length=2)

        print_result(f"\nБіграми {mode}")
        print_result(f"Кількість біграм: {sum(bigram_counts.values())}")
        print_result(f"H2 = {h2:.6f} біт/символ")
        r2 = 1 - h2 / h0
        print_result(f"Надлишковість за H2 = {r2:.2%}")
        print_result("П'ять найчастіших біграм:")
        print_top_five(bigram_counts)


# 3. Дослідження впливу розподілу символів на ентропію
length = 100_000

text_a = text_with_spaces[:length]
text_b = "а" * length
text_c = "".join(choice(alphabet) for _ in range(length))

for name, sequence in [
    ("А — природний текст", text_a),
    ("Б — повторення однієї літери", text_b),
    ("В — випадкові символи", text_c),
]:
    counts = Counter(sequence)
    h1 = calculate_entropy(counts)
    print_result(f"\n{name}: H1 = {h1:.6f} біт/символ")


# 4. Дослідження залежностей між символами
text_d = "аб" * 50_000

symbols = list(text_d)
shuffle(symbols)
text_g = "".join(symbols)

for name, sequence in [
    ("Г — випадковий порядок", text_g),
    ("Д — періодична послідовність", text_d),
]:
    print_result(f"\n{name}")

    counts = Counter(sequence)
    h1 = calculate_entropy(counts)
    print_result(f"H1 = {h1:.6f} біт/символ")

    for step in [1, 2]:
        mode = "з перетином" if step == 1 else "без перетину"
        bigram_counts = Counter()

        for i in range(0, len(sequence) - 1, step):
            bigram = sequence[i:i + 2]
            bigram_counts[bigram] += 1

        h2 = calculate_entropy(bigram_counts, block_length=2)
        print_result(f"H2 {mode} = {h2:.6f} біт/символ")


# 5. Експериментальна оцінка ентропії джерела
coolpink_results = [
    (10, 1.84512544126353, 2.72444203526882),
    (20, 1.87722292509504, 2.60192809488736),
    (30, 1.79475571203854, 2.54892637907445),
]


# 6. Оцінювання надлишковості джерела
# Алфавіт програми: 31 літера (без ё та ъ) і пробіл.
h0 = log2(32)

for order, h_lower, h_upper in coolpink_results:
    r_lower = 1 - h_upper / h0
    r_upper = 1 - h_lower / h0

    print_result(f"\nCoolPink, порядок {order}")
    print_result(f"{h_lower:.6f} < H < {h_upper:.6f} біт/символ")
    print_result(f"{r_lower:.2%} < R < {r_upper:.2%}")


# Збереження виводу у results.txt
with open("results.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(output_lines) + "\n")
