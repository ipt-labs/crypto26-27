import os
import matplotlib.pyplot as plt

from src.attack import RUS_FREQS
from src.vigenere import clean_text
from src.stats import avg_ic_for_r, calc_dr

os.makedirs("plots", exist_ok=True)

with open("data/ciphertext_v10.txt", "r", encoding="utf-8") as file:
    ciphertext = clean_text(file.read())

if len(ciphertext) < 32:
    raise SystemExit("Шифртекст надто короткий для побудови графіків.")

I_LANG = sum(p * p for p in RUS_FREQS.values())
I_RANDOM = 1 / 32
r_values = list(range(2, min(30, len(ciphertext) - 1) + 1))
ic_values = [avg_ic_for_r(ciphertext, r) for r in r_values]
dr_values = [calc_dr(ciphertext, r) / (len(ciphertext) - r)
             for r in r_values]

plt.figure(figsize=(10, 5))
plt.plot(r_values, ic_values, marker="o", linewidth=1.5)
plt.axhline(I_LANG, linestyle="--",
            label=f"IC мови за КП №1 = {I_LANG:.4f}")
plt.axhline(I_RANDOM, linestyle=":",
            label=f"IC випадкового тексту = {I_RANDOM:.5f}")
plt.xlabel("Кандидат періоду r")
plt.ylabel("Середній індекс відповідності")
plt.title("Середній IC залежно від кандидата періоду (варіант 10)")
plt.xticks(r_values)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("plots/ic_dependence.png", dpi=300)
plt.close()

plt.figure(figsize=(10, 5))
plt.bar(r_values, dr_values)
plt.xlabel("Відстань r")
plt.ylabel("Нормована кількість збігів D_r/(N-r)")
plt.title("Нормована статистика збігів D_r (варіант 10)")
plt.xticks(r_values)
plt.grid(True, linestyle="--", alpha=0.5, axis="y")
plt.tight_layout()
plt.savefig("plots/dr_dependence.png", dpi=300)
plt.close()

print("Графіки збережено у папці plots/.")
