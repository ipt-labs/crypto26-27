import os
from collections import Counter

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
KEYS = {
    "r2": "ор",
    "r3": "мир",
    "r4": "нога",
    "r5": "взлом",
    "r12": "криптография",
}

def encrypt(text, key):
    key_indices = [ALPHABET.index(c) for c in key]
    result = []
    for i, ch in enumerate(text):
        result.append(ALPHABET[(ALPHABET.index(ch) + key_indices[i % len(key)]) % M])
    return "".join(result)

def coincidence_index(text):
    n = len(text)
    counts = Counter(text)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))

def load_text(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    return "".join(c for c in raw)

def main():
    text = load_text("text_no_spaces.txt")
    results = {"plaintext": coincidence_index(text)}

    for name, key in KEYS.items():
        ciphertext = encrypt(text, key)
        results[name] = coincidence_index(ciphertext)
        with open(os.path.join(".", f"cipher_{name}.txt"), "w", encoding="utf-8") as f:
            f.write(ciphertext)

    for name, value in results.items():
        print(f"{name}: I = {value:.6f}")

if __name__ == "__main__":
    main()