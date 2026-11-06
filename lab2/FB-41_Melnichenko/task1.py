from collections import Counter

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
text = open("garri_potter_i_orden_feniksa.u_готово.txt", encoding="utf-8").read()
text = "".join(c for c in text if c in alphabet)[:1500]
open("text.txt", "w", encoding="utf-8").write(text)
def encrypt(text, key):
    return "".join(
        alphabet[(alphabet.index(c) +
                  alphabet.index(key[i % len(key)])) % 32]
        for i, c in enumerate(text)
    )
def coincidence(text):
    counts = Counter(text)
    n = len(text)
    return sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))
keys = ["мы", "кот", "лиса", "тайна", "криптография"]
results = [
    f"Довжина тексту: {len(text)} літер",
    f"Обсяг у UTF-8: {len(text.encode('utf-8'))} байтів",
    f"Відкритий текст: I = {coincidence(text):.6f}"
]
for key in keys:
    encrypted = encrypt(text, key)
    open(f"encrypted_{len(key)}.txt", "w",
         encoding="utf-8").write(encrypted)
    results.append(
        f"Ключ: {key}, r = {len(key)}, I = {coincidence(encrypted):.6f}"
    )
result = "\n".join(results)
print(result)
open("results_task1.txt", "w", encoding="utf-8").write(result)
