import math
import random
from collections import Counter


def entropy(t):
    return sum(-k / len(t) * math.log2(k / len(t)) for k in Counter(t).values())


random.seed(1872)
t = open("text_spaces.txt", encoding="utf-8").read()
N = 200000
a = t[:N]
b = "о" * N
v = "".join(random.choices(sorted(set(t)), k=N))

print(f"H0 = {math.log2(len(set(t))):.4f}")
for name, s in (("А", a), ("Б", b), ("В", v)):
    print(f"{name}: H1 = {entropy(s):.4f}")
