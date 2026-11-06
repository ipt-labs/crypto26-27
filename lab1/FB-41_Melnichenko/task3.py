import math
import random
from collections import Counter
from pathlib import Path

folder = Path(__file__).resolve().parent
text = (folder / "garri_potter_i_orden_feniksa.u_готово.txt").read_text(encoding="utf-8")
text = text.replace(" ", "")
alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
random.seed(8)
a = text[:100000]
b = "а" * len(a)
c = "".join(random.choices(alphabet, k=len(a)))

def entropy(text):
    counts = Counter(text)
    probabilities = [count / len(text) for count in counts.values()]
    return -sum(p * math.log2(p) for p in probabilities)
with open(folder / "results_task3.txt", "w", encoding="utf-8") as file:
    for name, sequence in [("А", a), ("Б", b), ("В", c)]:
        h = entropy(sequence)
        file.write(f"{name}: довжина = {len(sequence)}, H1 = {h:.6f} біт/символ\n")
print("Готово")
