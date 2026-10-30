import re
from collections import Counter

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
m = len(alphabet)

# підготовка тексту
def clean_text(file_path):
    f = open(file_path, "r", encoding="utf-8")
    raw = f.read().lower()
    f.close()

    raw = raw.replace("ё", "е")
    text = re.sub(r"[^а-я]", "", raw)  # залишаємо тільки літери
    return text


# шифрування шифром Віженера
def vigenere_encrypt(text, key):
    result = ""
    for i in range(len(text)):
        x = alphabet.index(text[i])
        k = alphabet.index(key[i % len(key)])
        y = (x + k) % m
        result += alphabet[y]
    return result

# розшифрування
def vigenere_decrypt(text, key):
    result = ""
    for i in range(len(text)):
        y = alphabet.index(text[i])
        k = alphabet.index(key[i % len(key)])
        x = (y - k) % m
        result += alphabet[x]
    return result

# індекс відповідності
def index_of_coincidence(text):
    n = len(text)
    if n < 2:
        return 0
    counts = Counter(text)
    s = 0
    for c in counts:
        s += counts[c] * (counts[c] - 1)
    return s / (n * (n - 1))

if __name__ == "__main__":

    # Завдання 1
    text = clean_text("animal_farm.txt")
    print("Довжина тексту:", len(text))
    print("Відкритий текст:", text[:60])
    print("I відкритого тексту:", round(index_of_coincidence(text), 5))
    print()

    keys = ["да", "лес", "море", "весна", "криптография"]
    for key in keys:
        ct = vigenere_encrypt(text, key)
        print(f"r = {len(key)}, ключ: {key}")
        print("шифртекст:", ct[:60])
        print(f"I = {index_of_coincidence(ct):.5f}\n")
    print()
