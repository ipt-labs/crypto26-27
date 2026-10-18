import argparse
 
ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
IDX = {c: i for i, c in enumerate(ALPHABET)}
 
 
def load(path):
    with open(path, encoding="utf-8") as f:
        text = f.read().lower().replace("ё", "е")
    return [IDX[c] for c in text if c in IDX]
 
 
def decrypt(y, key):
    return [(y[i] - key[i % len(key)]) % M for i in range(len(y))]
 
 
def to_str(seq):
    return "".join(ALPHABET[i] for i in seq)
 
 
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="cipher.txt")
    ap.add_argument("--key", default="последнийдозор", help="правильний ключ")
    ap.add_argument("--pos", type=int, default=3, help="позиція зміненої літери (з 0)")
    ap.add_argument("--delta", type=int, default=1, help="зсув літери ключа (mod 32)")
    args = ap.parse_args()
 
    y = load(args.file)
    key = [IDX[c] for c in args.key.lower()]
    r, n = len(key), len(y)
    bad = key[:]
    bad[args.pos] = (bad[args.pos] + args.delta) % M
 
    print("--- ПРОГНОЗ ---")
    print(f"Змінюється лише k_{args.pos}. Помилково розшифруються тільки позиції "
          f"i ≡ {args.pos} (mod {r}), тобто ≈ 1/{r} тексту (~{n // r} літер), "
          f"усі зі зсувом -({args.delta}) mod {M}. Решта тексту залишиться правильною.\n")
 
    ok, ko = decrypt(y, key), decrypt(y, bad)
    diff = [i for i in range(n) if ok[i] != ko[i]]
    shifts = {(ko[i] - ok[i]) % M for i in diff}
 
    print("--- РЕЗУЛЬТАТ ---")
    print(f"Правильний ключ: {to_str(key)}")
    print(f"Помилковий ключ: {to_str(bad)}")
    print(f"Відрізняється позицій: {len(diff)} з {n} ({100*len(diff)/n:.2f}%), очікувалось ≈ {100/r:.2f}%")
    print(f"Усі відмінності на i ≡ {args.pos} (mod {r}): {all(i % r == args.pos % r for i in diff)}")
    print(f"Зсув літер (mod {M}): {shifts}  (очікувалось {{{(-args.delta) % M}}})\n")
    print("Правильно:\n" + to_str(ok[:140]))
    print("З помилкою:\n" + to_str(ko[:140]))
    print("Зміни:\n" + "".join('^' if ok[i] != ko[i] else ' ' for i in range(140)))
    with open("decrypted_wrong.txt", "w", encoding="utf-8") as f:
        f.write(to_str(ko))
 
 
if __name__ == "__main__":
    main()
 