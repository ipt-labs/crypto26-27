import os

LETTERS = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(LETTERS)
CHAR_TO_IDX = {c: i for i, c in enumerate(LETTERS)}
IDX_TO_CHAR = {i: c for i, c in enumerate(LETTERS)}

DEFAULT_FILENAME = "6var.txt"
ORIGINAL_KEY = "возвращениеджинна"

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
    n = len(ciphertext)
    r = len(ORIGINAL_KEY)

    err_index = 0
    err_char = "г"
    corrupted_key = list(ORIGINAL_KEY)
    corrupted_key[err_index] = err_char
    corrupted_key = "".join(corrupted_key)

    clean_text = decrypt_vigenere(ciphertext, ORIGINAL_KEY)
    corrupted_text = decrypt_vigenere(ciphertext, corrupted_key)

    diff_count = sum(1 for c1, c2 in zip(clean_text, corrupted_text) if c1 != c2)
    expected_count = (n + (r - 1 - err_index)) // r
    diff_percentage = (diff_count / n) * 100

    print("=== ДОСЛІДЖЕННЯ ВПЛИВУ ПОМИЛКИ У КЛЮЧІ ===")
    print(f"Оригінальний ключ:  \"{ORIGINAL_KEY}\"")
    print(f"Ключ із помилкою:   \"{corrupted_key}\" (зміна на позиції {err_index + 1}: '{ORIGINAL_KEY[err_index]}' -> '{err_char}')\n")
    print(f"Загальна довжина тексту N:           {n}")
    print(f"Теоретично очікувано спотворень:    {expected_count} (~1/{r} або {100 / r:.2f}%)")
    print(f"Фактично отримано спотворень:       {diff_count} ({diff_percentage:.2f}%)\n")

    print("Порівняння перших 120 символів:")
    print("-" * 75)
    print("Правильний текст:")
    print(clean_text[:120])
    print("\nТекст із помилкою в ключі:")
    print(corrupted_text[:120])
    print("-" * 75)

if __name__ == "__main__":
    main()