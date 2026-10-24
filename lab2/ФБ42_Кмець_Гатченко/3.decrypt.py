from pathlib import Path
from collections import Counter

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

PERIOD = 16


def decrypt(text, key):
    result = ""
    for i, char in enumerate(text):
        y = ALPHABET.index(char)
        k = ALPHABET.index(key[i % len(key)])
        result += ALPHABET[(y - k) % 32]
    return result


if __name__ == "__main__":
    input_file1 = "variant5.txt"
    output_file1="decrypted.txt"
    with open(input_file1, 'r', encoding='utf-8') as f:
        text = f.read()
    top_letters = []
    for j in range(PERIOD):
        counts = Counter(text[j::PERIOD])
        top = sorted(counts, key=lambda char: (-counts[char], ALPHABET.index(char)))
        top_letters.append((top[0], counts[top[0]]))

    initial_key = ""
    for char, count in top_letters:
        shift = (ALPHABET.index(char) - ALPHABET.index("о")) % 32
        initial_key += ALPHABET[shift]
    print("Початковий ключ:", initial_key)
    print("Початок розшифрування:")
    print(decrypt(text, initial_key)[:76])

    corrections = {3, 4, 7, 13, 14}
    key = ""
    print("Блок  n    y*  Кількість  x*  Символ ключа")
    for j, (char, count) in enumerate(top_letters):
        assumed = "е" if j + 1 in corrections else "о"
        shift = (ALPHABET.index(char) - ALPHABET.index(assumed)) % 32
        key += ALPHABET[shift]
        print(f"{j + 1:>4}  {len(text[j::PERIOD])}   {char}      {count:>2}     {assumed}       {ALPHABET[shift]}")

    plaintext = decrypt(text, key)
    print("Відновлений ключ:", key)
    print("Розшифровано літер:", len(plaintext))
    print("Початок тексту:")
    print(plaintext[:76])
    print(plaintext[76:152])
    encoded_again = ""
    for i, char in enumerate(plaintext):
        x = ALPHABET.index(char)
        k = ALPHABET.index(key[i % PERIOD])
        encoded_again += ALPHABET[(x + k) % 32]
    print("Повторне шифрування збігається:", encoded_again == text)
    with open(output_file1, 'w', encoding='utf-8') as f:
                f.write(plaintext + "\n")
