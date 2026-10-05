import math
import random
from collections import Counter


def calculate_h1(text: str) -> float:

    n = len(text)
    if n == 0:
        return 0.0
    freqs = Counter(text)
    return -sum((count / n) * math.log2(count / n) for count in freqs.values())


def run_experiment(input_filepath: str):

    try:
        with open(input_filepath, "r", encoding="utf-8") as f:
            seq_a = f.read().strip()
    except FileNotFoundError:
        print(f"Файл {input_filepath} не знайдено.")
        return

    n = len(seq_a)
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    m = len(alphabet)

    seq_b = alphabet[0] * n

    random.seed(42)  
    seq_v = "".join(random.choice(alphabet) for _ in range(n))

    # Обчислення H1
    h1_a = calculate_h1(seq_a)
    h1_b = calculate_h1(seq_b)
    h1_v = calculate_h1(seq_v)
    h1_max = math.log2(m)

    print(f"Довжина послідовностей (N): {n} символів")
    print(f"Потужність алфавіту (m): {m} символів")
    print(f"Теоретичний максимум H_max = log2({m}): {h1_max:.6f} біт/символ\n")

    print(f"1. Послідовність Б (один символ):    H1 = {h1_b:.6f} біт/символ")
    print(f"2. Послідовність А (природний текст): H1 = {h1_a:.6f} біт/символ")
    print(f"3. Послідовність В (рівноймовірні):  H1 = {h1_v:.6f} біт/символ")


if __name__ == "__main__":

    run_experiment("output_without_spaces.txt")