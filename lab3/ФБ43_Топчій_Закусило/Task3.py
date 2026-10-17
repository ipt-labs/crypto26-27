import math
from collections import Counter
from Task1 import solve_congruence

M = 31
M2 = M * M
ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя"
LANG_TOP5 = ["ст", "но", "то", "на", "ен"]

def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def clean(text):
    return "".join(ch for ch in text if "а" <= ch <= "я")

def num(bg):
    return ALPHABET.index(bg[0]) * M + ALPHABET.index(bg[1])

text = clean(read_file("ishodniki/06_varik_UTF8.txt"))

extra = set(text) - set(ALPHABET)
missing = set(ALPHABET) - set(text)
if extra or missing:
    print(f"alphabet mismatch: extra={sorted(extra)} missing={sorted(missing)}")
    raise SystemExit

cipher_top5 = [bg for bg, _ in Counter(
    text[i:i + 2] for i in range(0, len(text) - 1, 2)).most_common(5)]
print(f"cipher top5: {cipher_top5}")

candidates = set()
for xs in LANG_TOP5:
    for xt in LANG_TOP5:
        if xs == xt:
            continue
        dx = num(xs) - num(xt)
        for ys in cipher_top5:
            for yt in cipher_top5:
                if ys == yt:
                    continue
                for a in solve_congruence(dx, num(ys) - num(yt), M2):
                    if math.gcd(a, M2) == 1:
                        candidates.add((a, (num(ys) - a * num(xs)) % M2))

print(f"candidates: {len(candidates)}")
for a, b in sorted(candidates):
    print(f"a={a}, b={b}")