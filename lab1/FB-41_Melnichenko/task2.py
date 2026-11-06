import csv
import math
from collections import Counter
from pathlib import Path

folder = Path(__file__).resolve().parent
text = (folder / "garri_potter_i_orden_feniksa.u_готово.txt").read_text(encoding="utf-8")
text_without_spaces = text.replace(" ", "")

def calculate(text, size, step):
    counts = Counter(text[i:i + size] for i in range(0, len(text) - size + 1, step))
    total = sum(counts.values())
    frequencies = {symbol: count / total for symbol, count in counts.items()}
    entropy = -sum(p * math.log2(p) for p in frequencies.values()) / size
    return counts, frequencies, entropy

with open(folder / "frequencies.csv", "w", encoding="utf-8-sig", newline="") as file, \
     open(folder / "results_task2.txt", "w", encoding="utf-8") as result:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Текст", "Тип", "Символ або біграма", "Кількість", "Частота"])

    for name, current in [("З пробілами", text), ("Без пробілів", text_without_spaces)]:
        result.write(f"{name}. Кількість символів: {len(current)}\n")
        entropies = []

        for label, size, step in [
            ("Символи", 1, 1),
            ("Біграми з перетином", 2, 1),
            ("Біграми без перетину", 2, 2)
        ]:
            counts, frequencies, entropy = calculate(current, size, step)
            entropies.append(entropy)

            result.write(f"\n{label}\n")
            result.write(f"Кількість: {sum(counts.values())}\n")
            result.write(f"H{size} = {entropy:.6f} біт/символ\n")
            result.write("П'ять найчастіших:\n")

            for symbol, count in counts.most_common():
                visible = symbol.replace(" ", "[пробіл]")
                writer.writerow([name, label, visible, count, f"{frequencies[symbol]:.10f}"])

            for symbol, count in counts.most_common(5):
                visible = symbol.replace(" ", "[пробіл]")
                result.write(f"{visible}: {count}; p = {frequencies[symbol]:.6f}\n")
        difference = abs(entropies[1] - entropies[2])
        result.write(f"\nРізниця між оцінками H2: {difference:.6f}\n\n")
print("Готово")
