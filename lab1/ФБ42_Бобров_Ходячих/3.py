from collections import Counter
import math
import os
import random
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cleaned_war_nospaces.txt")

with open(file_path, "r", encoding="utf-8") as f:
    full_text = f.read()

N = 100000

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
m = len(alphabet)

seq_A = full_text[:N]  # природний текст
seq_B = "а" * N  # повторення одного символу "а"
random.seed(26)
seq_V = "".join(random.choices(alphabet, k=N)) # випадкові рівноймовірні

def calculate_h1(sequence):
    total = len(sequence)
    counts = Counter(sequence)
    freqs = [count / total for count in counts.values()]
    return -sum(p * math.log2(p) for p in freqs if p > 0)

print(f"H1(А) = {calculate_h1(seq_A):.6f}")
print(f"H1(Б) = {calculate_h1(seq_B):.6f}")
print(f"H1(В) = {calculate_h1(seq_V):.6f}")