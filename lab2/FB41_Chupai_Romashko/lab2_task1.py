from collections import Counter

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"   
M = len(ALPHABET)                                
IDX = {ch: i for i, ch in enumerate(ALPHABET)}   


def clean_text(raw: str) -> str:
    text = raw.lower().replace("ё", "е")
    return "".join(ch for ch in text if ch in IDX)   


def vigenere_encrypt(text: str, key: str) -> str:
    r = len(key)
    return "".join(ALPHABET[(IDX[ch] + IDX[key[i % r]]) % M] for i, ch in enumerate(text))


def index_of_coincidence(text: str) -> float:
    n = len(text)
    counts = Counter(text)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))


if __name__ == "__main__":
    with open("text_task1.txt", encoding="utf-8", errors="ignore") as f:
        plain = clean_text(f.read())

    keys = ["ум", "лес", "ночь", "книга", "криптография"]   

    print(f"Довжина відкритого тексту: {len(plain)} літер\n")
    print(f"{'Текст':28s} {'I':>9s}")
    print("-" * 38)
    print(f"{'Відкритий текст':28s} {index_of_coincidence(plain):9.5f}")
    for key in keys:
        cipher = vigenere_encrypt(plain, key)
        print(f"{'r=' + str(len(key)) + ', ключ «' + key + '»':28s} {index_of_coincidence(cipher):9.5f}")