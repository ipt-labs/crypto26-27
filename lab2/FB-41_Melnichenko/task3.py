from collections import Counter

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
text = open("text_8.txt", encoding="utf-8").read()
r = 20

def decrypt(text, key):
    return "".join(alphabet[(alphabet.index(c) - alphabet.index(key[i % len(key)])) % 32]
        for i, c in enumerate(text)
    )

key_initial = ""
results = ["Блок;Три найчастіші літери (кількість);Літера ключа за о"]
for i in range(r):
    counts = Counter(text[i::r])
    top = counts.most_common(3)
    shift = (alphabet.index(top[0][0]) - alphabet.index("о")) % 32
    letter = alphabet[shift]
    key_initial += letter
    statistics = ", ".join(f"{c}: {n}" for c, n in top)
    results.append(f"{i + 1};{statistics};{letter}")
results += [
    "",
    f"Початковий ключ: {key_initial}",
    "Початкове розшифрування (перші 200 літер):",
    decrypt(text, key_initial)[:200]
]
key = "улановсеребряныепули"
decoded = decrypt(text, key)
encrypted = "".join(
    alphabet[(alphabet.index(c) +
              alphabet.index(key[i % r])) % 32]
    for i, c in enumerate(decoded)
)
results += [
    "",
    f"Уточнений ключ: {key}",
    f"Повторне шифрування збігається з початковим: {encrypted == text}",
    "Розшифрований текст (перші 600 літер):",
    decoded[:600]
]
open("key.txt", "w", encoding="utf-8").write(key)
open("decoded_8.txt", "w", encoding="utf-8").write(decoded)
result = "\n".join(results)
print(result)
open("results_task3.txt", "w", encoding="utf-8").write(result)
