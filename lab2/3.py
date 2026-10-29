ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
IDX = {c: i for i, c in enumerate(ALPHABET)}
def clean(text):
    text = text.lower().replace("ё", "е")
    return "".join(c for c in text if c in IDX)
def decrypt(text, key):
    r = len(key)
    return "".join(ALPHABET[(IDX[c] - IDX[key[i % r]]) % M] for i, c in enumerate(text))
def top_letters(block, k=3):
    counts = {}
    for c in block:
        counts[c] = counts.get(c, 0) + 1
    return sorted(counts.items(), key=lambda t: -t[1])[:k]

with open("v3.txt", encoding="utf-8", errors="ignore") as f:
    y = clean(f.read())

R = 14  

print("блок | топ-3 літери (частота %)        | ключова літера (x*='о')")
print("-" * 65)

key_guess = ""
for i in range(R):
    block = y[i::R]
    top = top_letters(block)
    
    y_star = top[0][0]
    
    k = (IDX[y_star] - IDX['о']) % M
    key_letter = ALPHABET[k]
    key_guess += key_letter
    
    info = ", ".join(f"{c}:{cnt / len(block) * 100:.1f}" for c, cnt in top)
    print(f"{i:>4} | {info:<32} | {key_letter}")

print("-" * 65)
print("Попередній згенерований ключ:", key_guess)
print("\nПочаток тексту з цим ключем:\n", decrypt(y, key_guess)[:200])

key = "экомаятникфуко"
print("\nІдеальний ключ:", key)
text = decrypt(y, key)
print("\nПочаток розшифрованого тексту:\n", text[:300])