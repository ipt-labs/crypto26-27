import csv
from pathlib import Path
from task1 import mod_inverse

folder = Path(__file__).resolve().parent
alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
n = len(alphabet) ** 2

text = (folder / "08.txt").read_text(encoding="utf-8-sig")
text = "".join(text.split()).lower()

numbers = [
    alphabet.index(text[i]) * 31 + alphabet.index(text[i + 1])
    for i in range(0, len(text), 2)
]

unlikely = {
    first + second
    for first in "аеиоуыэюяь"
    for second in "ьы"
}

def decrypt(a, b):
    inverse = mod_inverse(a, n)
    result = []

    for y in numbers:
        x = inverse * (y - b) % n
        result.append(alphabet[x // 31] + alphabet[x % 31])

    return "".join(result)

def check_text(text):
    common = sum(text.count(c) for c in "оеа") / len(text)
    rare = sum(text.count(c) for c in "фщ") / len(text)
    bad = sum(
        text[i:i + 2] in unlikely
        for i in range(len(text) - 1)
    ) / (len(text) - 1)

    accepted = common > 0.20 and rare < 0.04 and bad < 0.01
    return accepted, common, rare, bad

with open(folder / "candidates_task3.csv",
          encoding="utf-8-sig") as file:
    keys = [
        (int(row["a"]), int(row["b"]))
        for row in csv.DictReader(file, delimiter=";")
    ]

accepted = []
checks = []

for a, b in keys:
    decrypted = decrypt(a, b)
    passed, common, rare, bad = check_text(decrypted)
    checks.append([
        a, b, f"{common:.6f}", f"{rare:.6f}",
        f"{bad:.6f}", "Так" if passed else "Ні"
    ])

    if passed:
        accepted.append((a, b, decrypted, common, rare, bad))
        (folder / f"decrypted_{a}_{b}.txt").write_text(
            decrypted, encoding="utf-8"
        )

with open(folder / "checks_task4.csv", "w",
          encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow([
        "a", "b", "Частота оеа", "Частота фщ",
        "Частка малоймовірних біграм", "Пройшов відбір"
    ])
    writer.writerows(checks)

lines = [
    "Варіант 8",
    f"Перевірено ключів: {len(keys)}",
    f"Відкинуто: {len(keys) - len(accepted)}",
    f"Пройшли відбір: {len(accepted)}"
]

for a, b, decrypted, common, rare, bad in accepted:
    lines.extend([
        f"\nКлюч: a = {a}, b = {b}",
        f"Сумарна частота о, е, а: {common:.6f}",
        f"Сумарна частота ф, щ: {rare:.6f}",
        f"Частка малоймовірних біграм: {bad:.6f}",
        f"Файл: decrypted_{a}_{b}.txt",
        "\nПерші 300 символів:",
        decrypted[:300]
    ])

result = "\n".join(lines)
(folder / "results_task4.txt").write_text(result, encoding="utf-8")
print(result)
