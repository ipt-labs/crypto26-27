import argparse
from collections import Counter
 
ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"  # m = 32, без ё
M = len(ALPHABET)
IDX = {c: i for i, c in enumerate(ALPHABET)}
 
# Частоти літер рос. мови (можна замінити на свої з практикуму №1)
FREQ = {
    'а': .0801, 'б': .0159, 'в': .0454, 'г': .0170, 'д': .0298, 'е': .0845,
    'ж': .0094, 'з': .0165, 'и': .0735, 'й': .0121, 'к': .0349, 'л': .0440,
    'м': .0321, 'н': .0670, 'о': .1097, 'п': .0281, 'р': .0473, 'с': .0547,
    'т': .0626, 'у': .0262, 'ф': .0026, 'х': .0097, 'ц': .0048, 'ч': .0144,
    'ш': .0073, 'щ': .0036, 'ъ': .0004, 'ы': .0190, 'ь': .0174, 'э': .0032,
    'ю': .0064, 'я': .0201,
}
P = [FREQ[c] for c in ALPHABET]
 
 
def load(path):
    with open(path, encoding="utf-8") as f:
        text = f.read().lower().replace("ё", "е")
    return [IDX[c] for c in text if c in IDX]
 
 
def ic(seq):
    n = len(seq)
    if n < 2:
        return 0.0
    return sum(v * (v - 1) for v in Counter(seq).values()) / (n * (n - 1))
 
 
def decrypt(y, key):
    return [(y[i] - key[i % len(key)]) % M for i in range(len(y))]
 
 
def to_str(seq):
    return "".join(ALPHABET[i] for i in seq)
 
 
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="cipher.txt")
    ap.add_argument("-r", type=int, default=14, help="довжина ключа")
    ap.add_argument("--key", default=None, help="ключ вручну (для корекції)")
    ap.add_argument("--out", default="decrypted.txt")
    args = ap.parse_args()
 
    y = load(args.file)
    r = args.r
    print(f"Довжина шифртексту: {len(y)}, r = {r}, I(Y) = {ic(y):.4f}\n")
 
    key = []
    for j in range(r):
        block = y[j::r]
        n = len(block)
        cnt = Counter(block)
 
        # Спосіб з методички: k = (y* - x*) mod m, x* = 'о'
        ystar = cnt.most_common(1)[0][0]
        k_simple = (ystar - IDX['о']) % M
 
        # Статистика M_k = sum_t p_t * f_{(t+k) mod m}(Y_j)
        scores = sorted(
            ((sum(P[t] * cnt.get((t + k) % M, 0) / n for t in range(M)), k)
             for k in range(M)), reverse=True)[:3]
 
        print(f"Y_{j}: n={n}, I={ic(block):.4f}, "
              f"найчастіша літера ШТ '{ALPHABET[ystar]}' -> k='{ALPHABET[k_simple]}' | "
              f"M_k: " + ", ".join(f"'{ALPHABET[k]}'={v:.4f}" for v, k in scores))
        key.append(scores[0][1])
 
    if args.key:
        key = [IDX[c] for c in args.key.lower()]
        print("\nВикористано ключ, заданий вручну.")
 
    print("\nКлюч:", to_str(key))
    plain = to_str(decrypt(y, key))
    print("\nПочаток відкритого тексту:\n" + plain[:400])
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(plain)
    print(f"\nПовний текст збережено у {args.out}")
 
 
if __name__ == "__main__":
    main()
 