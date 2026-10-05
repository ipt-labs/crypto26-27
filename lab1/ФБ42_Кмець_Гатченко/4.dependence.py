import random
from collections import Counter
from math import log2

PATTERN = "ab"   # періодичний фрагмент
N = 10000      # довжина послідовностей
SEED = 42


def entropy(counter):
    total = sum(counter.values())
    return -sum((c / total) * log2(c / total) for c in counter.values()) + 0.0


def bigrams(seq, overlapping=True):
    step = 1 if overlapping else 2
    return [seq[i:i + 2] for i in range(0, len(seq) - 1, step)]


def h1(seq):
    return entropy(Counter(seq))


def h2(seq, overlapping=True):
    return entropy(Counter(bigrams(seq, overlapping))) / 2


random.seed(SEED)
D = (PATTERN * (N // len(PATTERN) + 1))[:N]   # періодична
letters = list(D)
random.shuffle(letters)
G = "".join(letters)                          # випадкова (ті самі частоти)

for name, s in (("Г", G), ("Д", D)):
    print(f"Послідовність {name}: довжина = {len(s)}, "
          f"H1 = {h1(s):.4f}, "
          f"H2 (з перетином) = {h2(s, True):.4f}, "
          f"H2 (без перетину) = {h2(s, False):.4f}")