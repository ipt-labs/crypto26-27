import os
from collections import Counter

# Робочий алфавіт
RUS_ALPH = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

# Словники для швидкого пошуку індексів (О(1) замість О(N))
CHAR_TO_IDX = {c: i for i, c in enumerate(RUS_ALPH)}
IDX_TO_CHAR = {i: c for i, c in enumerate(RUS_ALPH)}


def prepare_text(raw_text: str) -> str:
    """Очищення та нормалізація вхідного тексту."""
    formatted_text = raw_text.lower().replace("ё", "е")
    # Використовуємо генератор для швидшого збирання рядка
    return "".join([char for char in formatted_text if char in CHAR_TO_IDX])


def vigenere_cipher(text: str, key: str, decrypt: bool = False) -> str:
    """Універсальна функція для шифрування та розшифрування Віженера."""
    output_chars = []
    alpha_size = len(RUS_ALPH)
    key_length = len(key)

    for idx, char in enumerate(text):
        msg_idx = CHAR_TO_IDX[char]
        shift_idx = CHAR_TO_IDX[key[idx % key_length]]

        if decrypt:
            new_idx = (msg_idx - shift_idx) % alpha_size
        else:
            new_idx = (msg_idx + shift_idx) % alpha_size

        output_chars.append(IDX_TO_CHAR[new_idx])

    return "".join(output_chars)


def get_coincidence_index(text_data: str) -> float:
    """Обчислення індексу збігу (IC) для заданого тексту."""
    text_len = len(text_data)
    if text_len <= 1:
        return 0.0

    char_counts = Counter(text_data)
    # Компактний підрахунок через генераторний вираз
    coincidences = sum(freq * (freq - 1) for freq in char_counts.values())

    return coincidences / (text_len * (text_len - 1))


def main():
    # Налаштування шляхів до файлу
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(base_dir, "piece.txt")

    # Зчитування та обробка
    with open(target_file, "r", encoding="utf-8") as file:
        source_text = file.read()

    clean_text = prepare_text(source_text)
    file_size_kb = os.path.getsize(target_file) / 1024

    # Вивід початкової статистики
    print("=== АНАЛІЗ ВХІДНОГО ФАЙЛУ ===")
    print(f"Символів до нормалізації: {len(source_text)}")
    print(f"Символів після нормалізації: {len(clean_text)}")
    print(f"Розмір файлу на диску: {file_size_kb:.2f} KB")
    print(f"Зріз тексту (перші 200 симв.):\n{clean_text[:200]}\n")

    # Ключі для тестування
    test_keys = ["но", "эта", "стая", "живая", "невообразимая"]
    encrypted_variants = {}

    print("=== ПРОЦЕС ШИФРУВАННЯ ===")
    for k in test_keys:
        ciphered = vigenere_cipher(clean_text, k)
        encrypted_variants[k] = ciphered

        print(f"Ключ: '{k}' (довжина {len(k)})")
        print(f"Шифртекст (перші 100 симв.): {ciphered[:100]}\n")

    print("=== ІНДЕКСИ ЗБІГУ (IC) ===")
    ic_plaintext = get_coincidence_index(clean_text)
    print(f"ВІДКРИТИЙ ТЕКСТ | IC = {ic_plaintext:.6f}")

    for k, cipher_text in encrypted_variants.items():
        current_ic = get_coincidence_index(cipher_text)
        print(f"ШИФРТЕКСТ (Ключ: {k:<12} | Довжина: {len(k):<2}) | IC = {current_ic:.6f}")


if __name__ == "__main__":
    main()