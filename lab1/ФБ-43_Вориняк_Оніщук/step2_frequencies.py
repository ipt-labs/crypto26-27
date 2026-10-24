import math
from collections import Counter


def entropy(c):
    n = sum(c.values())
    return sum(-k / n * math.log2(k / n) for k in c.values())


def bigrams(t, step):
    return Counter(a + b for a, b in zip(t[::step], t[1::step]))


for name in ("text_spaces.txt", "text_nospaces.txt"):
    t = open(name, encoding="utf-8").read()
    c = Counter(t)
    print(name)
    for s, k in c.most_common():
        print(f"  {s!r} {k} {k / len(t):.5f}")
    print(f"H0 = {math.log2(len(c)):.4f}")
    print(f"H1 = {entropy(c):.4f}")
    for step, kind in ((1, "з перетином"), (2, "без перетину")):
        b = bigrams(t, step)
        n = sum(b.values())
        print(f"{kind}: {n} біграм, топ-5:", ", ".join(f"{p!r} {k / n:.5f}" for p, k in b.most_common(5)))
        print(f"H2 = {entropy(b) / 2:.4f}")

b = bigrams(open("text_spaces.txt", encoding="utf-8").read(), 1)
abc = sorted({p[0] for p in b})
with open("bigrams.csv", "w", encoding="utf-8") as f:
    f.write(";" + ";".join(abc) + "\n")
    for x in abc:
        f.write(x + ";" + ";".join(str(b[x + y]) for y in abc) + "\n")
print("жы, шы, чя:", b["жы"], b["шы"], b["чя"])
