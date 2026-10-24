import math
import random
from collections import Counter


def entropy(c):
    n = sum(c.values())
    return sum(-k / n * math.log2(k / n) for k in c.values())


def bigrams(t, step):
    return Counter(a + b for a, b in zip(t[::step], t[1::step]))


random.seed(1872)
for block in ("бесы", "бесов"):
    d = block * (120000 // len(block))
    g = "".join(random.sample(d, len(d)))
    for name, s in (("Г", g), ("Д", d)):
        h1 = entropy(Counter(s))
        print(f"{name} ({block}): H1 = {h1:.4f}, H2 = {entropy(bigrams(s, 1)) / 2:.4f} / {entropy(bigrams(s, 2)) / 2:.4f}")
