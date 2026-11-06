import csv
from collections import Counter

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
text = open("Crypto_CP2_variants-8-9.txt", encoding="utf-8-sig").read()
text = text.split("Вариант 8")[1]
text = "".join(c for c in text if c in alphabet)
open("text_8.txt", "w", encoding="utf-8").write(text)

def coincidence(text):
    counts = Counter(text)
    n = len(text)
    return sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))

rows = csv.reader(
    open("frequencies.csv", encoding="utf-8-sig"), delimiter=";"
)
frequencies = [
    float(row[4]) for row in rows
    if row[0] == "Без пробілів" and row[1] == "Символи"
]
language_index = sum(p ** 2 for p in frequencies)
results = [
    f"Довжина шифртексту: {len(text)} літер",
    f"Індекс відповідності шифртексту: {coincidence(text):.6f}",
    f"Орієнтир за частотами з КП1: {language_index:.6f}",
    f"Рівноймовірний алфавіт: {1 / 32:.6f}",
    "",
    "r;Середній індекс відповідності блоків"
]
for r in range(2, 31):
    indices = [coincidence(text[i::r]) for i in range(r)]
    average = sum(indices) / r
    results.append(f"{r};{average:.6f}")
result = "\n".join(results)
print(result)
open("results_task2.txt", "w", encoding="utf-8").write(result)
