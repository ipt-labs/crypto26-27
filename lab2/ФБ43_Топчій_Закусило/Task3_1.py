from collections import Counter
from task1 import ALPHABET, M, encrypt, load_text

R = 17

def caesar_shift(block, plaintext_letter="о"):
    counts = Counter(block)
    y_star = max(counts, key=counts.get)
    return (ALPHABET.index(y_star) - ALPHABET.index(plaintext_letter)) % M

def decrypt(text, key):
    inverse_key = "".join(ALPHABET[(-ALPHABET.index(c)) % M] for c in key)
    return encrypt(text, inverse_key)

def main():
    text = load_text("variant6.txt")
    blocks = [text[i::R] for i in range(R)]

    key_indices = [caesar_shift(b) for b in blocks]
    key = "".join(ALPHABET[k] for k in key_indices)
    print(f"key: {key}")

    decrypted = decrypt(text, key)
    print(f"head: {decrypted[:300]}")

    for i, b in enumerate(blocks):
        top3 = ", ".join(f"{c}:{n}" for c, n in Counter(b).most_common(3))
        print(f"block {i:2d}: {top3}")

if __name__ == "__main__":
    main()