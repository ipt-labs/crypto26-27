import sys
from collections import Counter
sys.path.insert(0, "../Lab1")
from task2 import read_file, char_frequencies
from Task1 import ALPHABET, M, encrypt, load_text

R = 17
LAB1_TEXT = "../Lab1/text_no_spaces.txt"

def letter_frequencies():
    text = read_file(LAB1_TEXT).replace("ё", "е")
    return {ch: p for ch, c, p in char_frequencies(text) if ch in ALPHABET}

FREQ = letter_frequencies()

def shift_scores(block):
    counts = Counter(block)
    return [
        sum(FREQ[ALPHABET[t]] * counts.get(ALPHABET[(t + k) % M], 0) for t in range(M))
        for k in range(M)
    ]

def decrypt(text, key):
    inverse = "".join(ALPHABET[(-ALPHABET.index(c)) % M] for c in key)
    return encrypt(text, inverse)

def main():
    print(f"frequencies from {LAB1_TEXT} (via Lab1/task2.py):")
    for ch in ALPHABET:
        print(f"  {ch}: {FREQ[ch]:.5f}")

    text = load_text("variant6.txt")
    blocks = [text[i::R] for i in range(R)]

    key_indices = []
    for i, b in enumerate(blocks):
        scores = shift_scores(b)
        ranked = sorted(range(M), key=lambda k: scores[k], reverse=True)
        key_indices.append(ranked[0])
        top3 = ", ".join(f"{ALPHABET[k]}:{scores[k]:.0f}" for k in ranked[:3])
        print(f"block {i:2d}: {top3}")

    key = "".join(ALPHABET[k] for k in key_indices)
    print(f"key: {key}")

    plain = decrypt(text, key)
    with open("decrypted.txt", "w", encoding="utf-8") as f:
        f.write(plain)
    print(f"head: {plain[:300]}")

if __name__ == "__main__":
    main()