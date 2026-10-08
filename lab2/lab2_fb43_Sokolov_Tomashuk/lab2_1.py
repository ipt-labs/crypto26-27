import collections
import os

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
CHAR_TO_INT = {ch: i for i, ch in enumerate(ALPHABET)}
INT_TO_CHAR = {i: ch for i, ch in enumerate(ALPHABET)}

MI = 0.0553
I0 = 1 / M


def clean_text(text: str) -> str:
    text = text.lower().replace("ё", "е")
    return "".join(ch for ch in text if ch in CHAR_TO_INT)


def calc_ic(text: str) -> float:
    n = len(text)
    if n <= 1:
        return 0.0
    counts = collections.Counter(text)
    return sum(cnt * (cnt - 1) for cnt in counts.values()) / (n * (n - 1))


def vigenere_encrypt(plaintext: str, key: str) -> str:
    r = len(key)
    return "".join(
        INT_TO_CHAR[(CHAR_TO_INT[ch] + CHAR_TO_INT[key[i % r]]) % M]
        for i, ch in enumerate(plaintext)
    )


def main():
    input_file = "lab2_crypt.txt"
    if not os.path.exists(input_file):
        print(f"Помилка: файл {input_file} не знайдено в поточній директорії!")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        plaintext = clean_text(f.read())

    keys_config = {2: "да", 3: "мир", 4: "зима", 5: "весна", 13: "криптосистема"}

    results = [("Відкритий текст", "-", len(plaintext), calc_ic(plaintext), MI)]
    for r, key in keys_config.items():
        cipher = vigenere_encrypt(plaintext, key)
        expected = MI / r + (1 - 1 / r) * I0      # теоретичне очікування для періоду r
        results.append((f"Шифртекст (r={r})", key, len(cipher), calc_ic(cipher), expected))

    line = "=" * 82
    print("РЕЗУЛЬТАТИ ДОСЛІДЖЕННЯ ШИФРУ ВІЖЕНЕРА (ЗАВДАННЯ 1)")
    print(line)
    print(f"{'Тип тексту':<22} | {'Ключ':<15} | {'Довжина':<8} | {'IC (факт)':<10} | {'IC (теорія)':<10}")
    print("-" * 82)
    for label, k, l, ic, ex in results:
        print(f"{label:<22} | {k:<15} | {l:<8} | {ic:<10.5f} | {ex:<10.5f}")
    print("-" * 82)
    print(f"Індекс відповідності мови (MI):          {MI:.4f}")
    print(f"Індекс випадкового тексту (I0 = 1/32):   {I0:.5f}")
    print("Теорія для періоду r: MI/r + (1 - 1/r) * I0")
    print()
    print("ПОЯСНЕННЯ:")
    print("Індекс відповідності відкритого тексту близький до теоретичного мовного значення.")
    print("Зі збільшенням періоду ключа r індекс спадає та наближається до 0.03125,")
    print("оскільки поліалфавітна підстановка згладжує нерівномірність частот природної мови.")


if __name__ == "__main__":
    main()