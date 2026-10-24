from pathlib import Path
from collections import Counter

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"


def normalize(text):
    text = text.lower().replace("ё", "е")
    return "".join(char for char in text if char in ALPHABET)


def encrypt(text, key):
    result = ""
    for i, char in enumerate(text):
        x = ALPHABET.index(char)
        k = ALPHABET.index(key[i % len(key)])
        result += ALPHABET[(x + k) % 32]
    return result


def coincidence_index(text):
    n = len(text)
    counts = Counter(text)
    return sum(count * (count - 1) for count in counts.values()) / (n * (n - 1))


if __name__ == "__main__":
    input_file = "lab2.txt"
    with open(input_file, 'r', encoding='utf-8') as f:
               source = f.read()
    text = normalize(source)

    print(f"Після підготовки: {len(text)} літер, {len(text.encode('utf-8'))} байтів")
    print(f"Індекс відкритого тексту: {coincidence_index(text):.6f}")
    print()
    print(f"{'Ключ':<16} {'r':>2}  {'Індекс шифртексту':>18}")
    for key in ["да", "мир", "ключ", "книга", "криптография"]:
        ciphertext = encrypt(text, key)
        print(f"{key:<16} {len(key):>2}  {coincidence_index(ciphertext):>18.6f}")
