import math
import random
from collections import Counter

def entropy_from_counts(counts: Counter, total: int) -> float:
    """Обчислення ентропії """
    h = 0.0
    for count in counts.values():
        p = count / total
        if p > 0:
            h -= p * math.log2(p)
    return h


def calculate_metrics(seq: str):
    n = len(seq)

    h1 = entropy_from_counts(Counter(seq), n)

    bigrams_overlap = [seq[i : i + 2] for i in range(n - 1)]
    h2_overlap = (
        entropy_from_counts(Counter(bigrams_overlap), len(bigrams_overlap)) / 2
    )

    bigrams_non_overlap = [seq[i : i + 2] for i in range(0, n - 1, 2)]
    h2_non_overlap = (
        entropy_from_counts(
            Counter(bigrams_non_overlap), len(bigrams_non_overlap)
        )
        / 2
    )

    return h1, h2_overlap, h2_non_overlap


def main():
    length = 1000

    seq_d = "ab" * (length // 2)

    half = length // 2
    chars_g = ["a"] * half + ["b"] * half
    random.seed(42)
    random.shuffle(chars_g)
    seq_g = "".join(chars_g)

    h1_g, h2_g_ov, h2_g_nov = calculate_metrics(seq_g)
    h1_d, h2_d_ov, h2_d_nov = calculate_metrics(seq_d)

    print(f"{'Метрика':<35} | {'Послідовність Г':<15} | {'Послідовність Д':<15}")
    print("-" * 72)
    print(f"{'H1 (ентропія символів)':<35} | {h1_g:<15.4f} | {h1_d:<15.4f}")
    print(
        f"{'H2 (біграми з перекриттям)':<35} | {h2_g_ov:<15.4f} | {h2_d_ov:<15.4f}"
    )
    print(
        f"{'H2 (біграми без перекриття)':<35} | {h2_g_nov:<15.4f} | {h2_d_nov:<15.4f}"
    )


if __name__ == "__main__":
    main()