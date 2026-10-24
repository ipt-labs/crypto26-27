import bz2
import math
from collections import Counter


def entropy(c):
    n = sum(c.values())
    return sum(-k / n * math.log2(k / n) for k in c.values())


for name in ("text_spaces.txt", "text_nospaces.txt"):
    t = open(name, encoding="utf-8").read()
    h0 = math.log2(len(set(t)))
    h1 = entropy(Counter(t))
    h2 = entropy(Counter(a + b for a, b in zip(t, t[1:]))) / 2
    bz = 8 * len(bz2.compress(t.encode("cp1251"))) / len(t)
    print(f"{name}: R(H1) = {1 - h1 / h0:.2%}, R(H2) = {1 - h2 / h0:.2%}, bz2 = {bz:.4f} біт/символ, R = {1 - bz / h0:.2%}")

coolpink = {10: (2.08319877272088, 2.75441571804231), 20: (1.93077228732386, 2.7479764393853), 30: (1.98674573021743, 2.59134159462775)}
for n, (low, high) in coolpink.items():
    print(f"H({n}): R = {1 - high / 5:.2%} ... {1 - low / 5:.2%}")
