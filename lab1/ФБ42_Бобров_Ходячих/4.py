from collections import Counter
import math
import random

alphabet = ["а", "б", "в", "г"]
N = 100000

seq_D = "".join(alphabet) * (N // len(alphabet))
random.seed(26)
seq_G = "".join(random.choices(alphabet, k=N))

def calc_stats(text, n, step):
    ngrams = [text[i : i + n] for i in range(0, len(text) - n + 1, step)]
    counts = Counter(ngrams)
    total = len(ngrams)
    freqs = {k: v / total for k, v in counts.items()}
    h = -sum(p * math.log2(p) for p in freqs.values() if p > 0) / n
    return h

print("--- ПОСЛІДОВНІСТЬ Г ---")
print(f"H1                    = {calc_stats(seq_G, n=1, step=1):.6f}")
print(f"H2 (перетинаються)    = {calc_stats(seq_G, n=2, step=1):.6f}")
print(f"H2 (не перетинаються) = {calc_stats(seq_G, n=2, step=2):.6f}\n")

print("--- ПОСЛІДОВНІСТЬ Д ---")
print(f"H1                    = {calc_stats(seq_D, n=1, step=1):.6f}")
print(f"H2 (перетинаються)    = {calc_stats(seq_D, n=2, step=1):.6f}")
print(f"H2 (не перетинаються) = {calc_stats(seq_D, n=2, step=2):.6f}")