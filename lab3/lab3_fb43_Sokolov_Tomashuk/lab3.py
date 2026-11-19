import csv
import os
import sys
from collections import Counter

from lab1_2 import calculate_bigram_entropy

HERE = os.path.dirname(os.path.abspath(__file__))

ALPHA = "абвгдежзийклмнопрстуфхцчшщыьэюя"
M = len(ALPHA)
M2 = M * M
IDX = {c: i for i, c in enumerate(ALPHA)}

TOP_RU = ["ст", "но", "то", "на", "ен"]


def egcd(a, b):
    u0, u1, v0, v1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return a, u0, v0


def inv(a, n):
    d, u, _ = egcd(a % n, n)
    return u % n if d == 1 else None


def solve_lin(a, b, n):
    a %= n
    b %= n
    d, _, _ = egcd(a, n)
    if b % d:
        return []
    a1, b1, n1 = a // d, b // d, n // d
    x0 = (b1 * inv(a1, n1)) % n1 if n1 > 1 else 0
    return [x0 + k * n1 for k in range(d)]


def bigram_to_num(s):
    return IDX[s[0]] * M + IDX[s[1]]


def num_to_bigram(x):
    return ALPHA[x // M] + ALPHA[x % M]


def top_bigrams(text, k=5):
    _, _, cnt, _ = calculate_bigram_entropy(text, step=2)
    return cnt.most_common(k), cnt


def load_ref_bigrams(k=20):
    path = os.path.join(HERE, "freqs_bigrams_overlap_without_spaces.csv")
    with open(path, encoding="utf-8") as f:
        rows = list(csv.reader(f))[1:k + 1]
    return {r[0] for r in rows}


REF_BIGRAMS = load_ref_bigrams()


def cross_share(text):
    bs = [text[i:i + 2] for i in range(1, len(text) - 1, 2)]
    return sum(b in REF_BIGRAMS for b in bs) * 100.0 / len(bs)


def decrypt(text, a, b):
    ai = inv(a, M2)
    out = []
    for i in range(0, len(text) - 1, 2):
        Y = bigram_to_num(text[i:i + 2])
        out.append(num_to_bigram((ai * (Y - b)) % M2))
    return "".join(out)

RU_FREQ = {
    'о': 10.97, 'е': 8.45 + 0.04, 'а': 8.01, 'и': 7.35, 'н': 6.70, 'т': 6.26,
    'с': 5.47, 'р': 4.73, 'в': 4.54, 'л': 4.40, 'к': 3.49, 'м': 3.21,
    'д': 2.98, 'п': 2.81, 'у': 2.62, 'я': 2.01, 'ы': 1.90, 'ь': 1.74 + 0.04,
    'г': 1.70, 'з': 1.65, 'б': 1.59, 'ч': 1.44, 'й': 1.21, 'х': 0.97,
    'ж': 0.94, 'ш': 0.73, 'ю': 0.64, 'ц': 0.48, 'щ': 0.36, 'э': 0.32,
    'ф': 0.26,
}
FORBIDDEN = ["аь", "оь", "уь", "еь", "иь", "ыь", "яь", "юь", "эь", "ьь",
             "ыы", "ьы", "ьй", "йь", "жы", "шы", "чы", "щы", "чя", "шя",
             "щя", "жя", "чю", "шю", "щю", "жю", "цю", "ця", "ыа", "ыо",
             "ыу", "ыэ", "ыю", "ыя", "ьэ", "эы", "йй", "йы", "ьъ"]
FREQ_N = 120


def score(text):
    n = len(text)
    cnt = Counter(text)
    dist = sum(abs(cnt.get(c, 0) * 100.0 / n - RU_FREQ[c]) for c in ALPHA)
    forb = sum(text.count(f) for f in FORBIDDEN) * 100.0 / n
    rare = sum(cnt.get(c, 0) for c in "фщэ") * 100.0 / n
    return dist, forb, rare, cross_share(text)


def is_meaningful(text):
    dist, forb, rare, cross = score(text)
    cnt = Counter(text)
    n = len(text)
    f = lambda c: cnt.get(c, 0) * 100.0 / n
    common = f('о') + f('а') + f('е')
    ok = common > 22 and rare < 2.0 and forb < 1.0 and dist < 40 and cross > 12
    return ok, (dist, forb, rare, common, cross)


def main(path):
    raw = open(path, encoding="utf-8").read()
    text = "".join(ch for ch in raw.lower() if ch in IDX)
    if len(text) % 2:
        text = text[:-1]
    print(f"Довжина шифртексту: {len(text)} літер, {len(text) // 2} біграм")
    top, cnt = top_bigrams(text, 5)
    print("5 найчастіших біграм шифртексту:")
    for bg, c in top:
        print(f"  {bg}  {c}  (число {bigram_to_num(bg)})")

    Xs = [bigram_to_num(b) for b in TOP_RU]
    Ys = [bigram_to_num(b) for b, _ in top]

    tried = set()
    found = []
    pairs = [(i, j) for i in range(5) for j in range(5) if i != j]
    n_cand = 0
    for (i, j) in ((i, j) for i in range(5) for j in range(i + 1, 5)):
        for (k, l) in pairs:
            X1, X2 = Xs[i], Xs[j]
            Y1, Y2 = Ys[k], Ys[l]
            for a in solve_lin((X1 - X2) % M2, (Y1 - Y2) % M2, M2):
                if egcd(a, M2)[0] != 1:
                    continue
                b = (Y1 - a * X1) % M2
                if (a, b) in tried:
                    continue
                tried.add((a, b))
                n_cand += 1
                pt = decrypt(text, a, b)
                ok, det = is_meaningful(pt)
                if ok:
                    found.append((a, b, (TOP_RU[i], TOP_RU[j]), (top[k][0], top[l][0]), det, pt))
    print(f"\nПеревірено кандидатів у ключ: {n_cand}")
    print(f"Пройшли розпізнавач: {len(found)}")
    for a, b, xp, yp, det, pt in found:
        print(f"\nКлюч (a, b) = ({a}, {b}); зіставлення {xp} -> {yp}")
        print("метрики (dist, forb%, rare%, о+а+е%, перетин%):", tuple(round(v, 2) for v in det))
        print(pt[:300])
    if found:
        a, b = found[0][0], found[0][1]
        open("decrypted_V1.txt", "w", encoding="utf-8").write(found[0][5])
        open("key_V1.txt", "w", encoding="utf-8").write(f"a = {a}\nb = {b}\n")
    return found


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "V1.txt")