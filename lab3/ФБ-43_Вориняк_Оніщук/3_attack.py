import sys
from importlib import import_module
from itertools import combinations, permutations

m1, m2 = import_module("1_modarith"), import_module("2_bigrams")
inverse, solve, bigrams, read = m1.inverse, m1.solve, m2.bigrams, m2.read

ABC = "абвгдежзийклмнопрстуфхцчшщыьэюя"
if "swap" in sys.argv:
    ABC = "абвгдежзийклмнопрстуфхцчшщьыэюя"
M, N = 31, 961


def to_nums(t):
    return [ABC.index(x) * M + ABC.index(y) for x, y in zip(t[::2], t[1::2])]


def decrypt(ys, a, b):
    a1 = inverse(a, N)
    return "".join(ABC[x // M] + ABC[x % M] for x in (a1 * (y - b) % N for y in ys))


def score(t):
    return sum(t.count(c) for c in "оае") / len(t), sum(t.count(c + "ь") for c in "аеиоуыэюяйь")


text = read(sys.argv[1])
ys = to_nums(text)
top = [bg for bg, _ in bigrams(text, 2).most_common(5)]

keys = set()
for x1, x2 in combinations(["ст", "но", "то", "на", "ен"], 2):
    for y1, y2 in permutations(top, 2):
        (X1, X2), (Y1, Y2) = to_nums(x1 + x2), to_nums(y1 + y2)
        for a in solve(X1 - X2, Y1 - Y2, N):
            if a % M:
                keys.add((a, (Y1 - a * X1) % N))
print("Кандидатів на ключ:", len(keys))

rejected = []
for a, b in sorted(keys):
    plain = decrypt(ys, a, b)
    freq, forb = score(plain)
    if freq >= 0.22 and forb == 0:
        print(f"Ключ ({a}, {b}): о+а+е = {freq:.4f}, заборонених біграм {forb}")
        print(plain[:100])
        open(sys.argv[1].replace(".txt", "_decrypted.txt"), "w", encoding="utf-8").write(plain)
    else:
        rejected.append((freq, forb))
print(f"Відкинуто {len(rejected)}: о+а+е не більше {max(f for f, _ in rejected):.4f}, "
      f"заборонених біграм не менше {min(z for _, z in rejected)}")
