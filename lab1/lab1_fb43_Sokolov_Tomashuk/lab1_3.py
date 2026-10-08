from collections import Counter
import math
import os
import random
import sys

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def calculate_h1(text):
    total_len = len(text)
    counts = Counter(text)
    h1 = 0.0
    for count in counts.values():
        p = count / total_len
        h1 -= p * math.log2(p)
    return h1, counts


def main():
    sample_len = 100000

    file_path = os.path.join(SCRIPT_DIR, "text_without_spaces.txt")
    if not os.path.exists(file_path):
        print(f"Помилка: не знайдено {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    seq_a = full_text[:sample_len]

    alphabet = sorted(list(set(full_text)))
    m = len(alphabet)

    seq_b = "а" * sample_len

    seq_c = "".join(random.choices(alphabet, k=sample_len))

    h1_a, counts_a = calculate_h1(seq_a)
    h1_b, counts_b = calculate_h1(seq_b)
    h1_c, counts_c = calculate_h1(seq_c)

    print("=" * 60)
    print("РЕЗУЛЬТАТИ ЕКСПЕРИМЕНТУ РОЗДІЛУ 3")
    print(f"Довжина вибірок: N = {sample_len} символів, Алфавіт: m = {m}")
    print("=" * 60)
    print(
        f"Послідовність Б (один символ 'а'):        H1 = {h1_b:.4f} біт/символ"
    )
    print(
        f"Послідовність А (природний текст):        H1 = {h1_a:.4f} біт/символ"
    )
    print(
        f"Послідовність В (випадкова рівноймовірна): H1 = {h1_c:.4f} біт/символ"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()