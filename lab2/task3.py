import os
from collections import Counter

LETTERS = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(LETTERS)
CHAR_TO_IDX = {c: i for i, c in enumerate(LETTERS)}
IDX_TO_CHAR = {i: c for i, c in enumerate(LETTERS)}

DEFAULT_FILENAME = "6var.txt"
DEFAULT_PERIOD = 17

def load_ciphertext(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read().lower().replace("ё", "е")
    return "".join(ch for ch in raw if ch in CHAR_TO_IDX)

def decrypt_vigenere(ciphertext: str, key: str) -> str:
    plaintext = []
    r = len(key)
    for idx, char in enumerate(ciphertext):
        y_val = CHAR_TO_IDX[char]
        k_val = CHAR_TO_IDX[key[idx % r]]
        m_val = (y_val - k_val) % M
        plaintext.append(IDX_TO_CHAR[m_val])
    return "".join(plaintext)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(base_dir, DEFAULT_FILENAME)

    if not os.path.exists(target_file):
        print(f"Помилка: файл '{DEFAULT_FILENAME}' не знайдено.")
        return

    ciphertext = load_ciphertext(target_file)

    known_plain = "дорофейльвовичпив"

    key_chars = []
    for i in range(17):
        y_val = CHAR_TO_IDX[ciphertext[i]]
        x_val = CHAR_TO_IDX[known_plain[i]]
        k_val = (y_val - x_val) % M
        key_chars.append(IDX_TO_CHAR[k_val])

    exact_key = "".join(key_chars)

    print(f"ТОЧНИЙ КЛЮЧ: \"{exact_key}\" (довжина: {len(exact_key)})")

    decrypted = decrypt_vigenere(ciphertext, exact_key)

    out_file = os.path.join(base_dir, "decrypted_6var.txt")
    with open(out_file, "w", encoding="utf-8") as out:
        out.write(decrypted)

    print(f"\nРезультат збережено в: decrypted_6var.txt")
    print("\nПерші 300 символів розшифрованого тексту:")
    print("-" * 75)
    print(decrypted[:300])
    print("-" * 75)

if __name__ == "__main__":
    main()