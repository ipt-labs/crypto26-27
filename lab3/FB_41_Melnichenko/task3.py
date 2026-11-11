import csv
from itertools import permutations
from math import gcd
from pathlib import Path
from task1 import solve_congruence

folder = Path(__file__).resolve().parent
alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
m = len(alphabet)
n = m ** 2

language_bigrams = ["ст", "но", "то", "на", "ен"]

with open(folder / "frequencies_task2.csv",
          encoding="utf-8-sig") as file:
    rows = list(csv.DictReader(file, delimiter=";"))

rows.sort(key=lambda row: int(row["Кількість"]), reverse=True)
cipher_bigrams = [row["Біграма"] for row in rows[:5]]

def bigram_number(bigram):
    return alphabet.index(bigram[0]) * m + alphabet.index(bigram[1])

keys = set()
comparisons = 0
without_solutions = 0
multiple_solutions = 0
rejected = 0

for first, second in permutations(language_bigrams, 2):
    x1 = bigram_number(first)
    x2 = bigram_number(second)

    for encrypted_first, encrypted_second in permutations(cipher_bigrams, 2):
        y1 = bigram_number(encrypted_first)
        y2 = bigram_number(encrypted_second)
        comparisons += 1

        solutions = solve_congruence(x1 - x2, y1 - y2, n)

        if not solutions:
            without_solutions += 1
        elif len(solutions) > 1:
            multiple_solutions += 1

        for a in solutions:
            if gcd(a, n) != 1:
                rejected += 1
                continue

            b = (y1 - a * x1) % n
            keys.add((a, b))

keys = sorted(keys)

with open(folder / "candidates_task3.csv", "w",
          encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["a", "b"])
    writer.writerows(keys)

lines = [
    f"Біграми мови: {', '.join(language_bigrams)}",
    f"Біграми шифртексту: {', '.join(cipher_bigrams)}",
    f"Кількість зіставлень: {comparisons}",
    f"Порівнянь без розв'язків: {without_solutions}",
    f"Порівнянь із декількома розв'язками: {multiple_solutions}",
    f"Відкинуто значень a, не взаємно простих із модулем: {rejected}",
    f"Кількість унікальних кандидатів на ключ: {len(keys)}",
    "\nПерші 10 кандидатів (a, b):"
]

for a, b in keys[:10]:
    lines.append(f"({a}, {b})")

result = "\n".join(lines)
(folder / "results_task3.txt").write_text(result, encoding="utf-8")
print(result)
