import math
from collections import Counter
from Task1 import mod_inverse, solve_congruence

M = 31
M2 = M * M
ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя"
CIPHER_FILE = "ishodniki/06_varik_UTF8.txt"
REFERENCE_FILE = "../Lab1/text_no_spaces.txt"

def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def clean(text):
    result = []
    for ch in text:
        if ch == "ё":
            ch = "е"
        if ch == "ъ":
            ch = "ь"
        if "а" <= ch <= "я":
            result.append(ch)
    return "".join(result)

def num(bg):
    return ALPHABET.index(bg[0]) * M + ALPHABET.index(bg[1])

def decrypt(text, a, b):
    ainv = mod_inverse(a, M2)
    out = []
    for i in range(0, len(text) - 1, 2):
        y = num(text[i:i + 2])
        x = ainv * (y - b) % M2
        out.append(ALPHABET[x // M] + ALPHABET[x % M])
    return "".join(out)

def build_reference(path):
    text = clean(read_file(path))
    counter = Counter(text[i:i + 2] for i in range(len(text) - 1))
    total = sum(counter.values())
    return {bg: c / total for bg, c in counter.items()}

def score(text, ref):
    bigrams = [text[i:i + 2] for i in range(len(text) - 1)]
    return sum(ref.get(bg, 0) for bg in bigrams) / len(bigrams)

ref = build_reference(REFERENCE_FILE)
cipher = clean(read_file(CIPHER_FILE))

candidates = set()
LANG_TOP5 = ["ст", "но", "то", "на", "ен"]
cipher_top5 = [bg for bg, _ in Counter(
    cipher[i:i + 2] for i in range(0, len(cipher) - 1, 2)).most_common(5)]
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

results = sorted(((a, b, score(decrypt(cipher, a, b), ref)) for a, b in candidates),
                 key=lambda t: t[2], reverse=True)

plain_ref = clean(read_file(REFERENCE_FILE))
print(f"reference score: {score(plain_ref, ref):.6f}")

print(f"tested: {len(results)} candidates")
for a, b, s in results[:10]:
    print(f"a={a}, b={b}, score={s:.6f}")

a, b, s = results[0]
plain = decrypt(cipher, a, b)
print(f"\nbest key: a={a}, b={b}")
print(plain[:200])
with open("decrypted.txt", "w", encoding="utf-8") as f:
    f.write(plain)