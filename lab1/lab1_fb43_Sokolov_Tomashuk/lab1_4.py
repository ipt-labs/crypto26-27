from collections import Counter
import math
import random
import sys

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")


def calculate_h1(text):
    total = len(text)
    counts = Counter(text)
    h1 = 0.0
    for cnt in counts.values():
        p = cnt / total
        h1 -= p * math.log2(p)
    return h1


def calculate_h2(text, step=1):
    bigrams = [text[i : i + 2] for i in range(0, len(text) - 1, step)]
    total = len(bigrams)
    counts = Counter(bigrams)
    h_pair = 0.0
    for cnt in counts.values():
        p = cnt / total
        h_pair -= p * math.log2(p)
    return h_pair / 2.0, counts


def main():
    sample_len = 100000

    seq_g = "".join(random.choices(["а", "б"], k=sample_len))

    seq_d = ("аб" * (sample_len // 2))[:sample_len]

    h1_g = calculate_h1(seq_g)
    h2_g_ov, counts_g_ov = calculate_h2(seq_g, step=1)
    h2_g_no, counts_g_no = calculate_h2(seq_g, step=2)

    h1_d = calculate_h1(seq_d)
    h2_d_ov, counts_d_ov = calculate_h2(seq_d, step=1)
    h2_d_no, counts_d_no = calculate_h2(seq_d, step=2)

    print("=" * 65)
    print("РЕЗУЛЬТАТИ ЕКСПЕРИМЕНТУ РОЗДІЛУ 4")
    print(f"Довжина послідовностей: N = {sample_len}")
    print("=" * 65)

    print("ПОСЛІДОВНІСТЬ Г (ВИПАДКОВА):")
    print(f"  H1 (ентропія літер):                   {h1_g:.4f} біт/символ")
    print(f"  H2 (біграми з перетином, крок 1):      {h2_g_ov:.4f} біт/символ")
    print(f"  H2 (біграми без перетину, крок 2):     {h2_g_no:.4f} біт/символ")
    print(f"  Знайдені біграми (з перетином):        {dict(counts_g_ov)}")

    print("\nПОСЛІДОВНІСТЬ Д (ПЕРІОДИЧНА 'abab...'):")
    print(f"  H1 (ентропія літер):                   {h1_d:.4f} біт/символ")
    print(f"  H2 (біграми з перетином, крок 1):      {h2_d_ov:.4f} біт/символ")
    print(f"  H2 (біграми без перетину, крок 2):     {h2_d_no:.4f} біт/символ")
    print(f"  Знайдені біграми (з перетином):        {dict(counts_d_ov)}")
    print(f"  Знайдені біграми (без перетину):       {dict(counts_d_no)}")
    print("=" * 65)


if __name__ == "__main__":
    main()