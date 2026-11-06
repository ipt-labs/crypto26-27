import math
import random
from collections import Counter
from pathlib import Path

def entropy(text, size, step):
    counts = Counter(text[i:i + size] for i in range(0, len(text) - size + 1, step))
    total = sum(counts.values())
    h = 0.0
    for count in counts.values():
        p = count / total
        h -= p * math.log2(p)
    return h / size

d = "аб" * 50000
letters = list(d)
random.seed(8)
random.shuffle(letters)
g = "".join(letters)

folder = Path(__file__).resolve().parent
with open(folder / "results_task4.txt", "w", encoding="utf-8") as file:
    for name, text in [("Г", g), ("Д", d)]:
        file.write(f"{name}\n")
        file.write(f"H1 = {entropy(text, 1, 1):.6f}\n")
        file.write(f"H2 з перетином = {entropy(text, 2, 1):.6f}\n")
        file.write(f"H2 без перетину = {entropy(text, 2, 2):.6f}\n\n")

print("Готово")