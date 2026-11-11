import csv
from collections import Counter
from pathlib import Path

folder = Path(__file__).resolve().parent
text = (folder / "08.txt").read_text(encoding="utf-8-sig")
text = "".join(text.split()).lower()

def calculate(text, size, step):
    counts = Counter(
        text[i:i + size]
        for i in range(0, len(text) - size + 1, step)
    )
    total = sum(counts.values())
    frequencies = {
        symbol: count / total
        for symbol, count in counts.items()
    }
    return counts, frequencies

counts, frequencies = calculate(text, 2, 2)

with open(folder / "frequencies_task2.csv", "w",
          encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Біграма", "Кількість", "Частота"])
    for bigram, count in counts.most_common():
        writer.writerow([bigram, count, f"{frequencies[bigram]:.10f}"])

lines = [
    "Варіант 8",
    f"Кількість символів: {len(text)}",
    f"Кількість біграм без перетину: {sum(counts.values())}",
    "\nП'ять найчастіших біграм:"
]

for bigram, count in counts.most_common(5):
    lines.append(f"{bigram}: {count}; p = {frequencies[bigram]:.6f}")

result = "\n".join(lines)
(folder / "results_task2.txt").write_text(result, encoding="utf-8")
print(result)
