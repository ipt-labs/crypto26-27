"""Реалізація шифру Віженера для російського алфавіту з 32 літер."""

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
CHAR_TO_IDX = {ch: i for i, ch in enumerate(ALPHABET)}
IDX_TO_CHAR = {i: ch for i, ch in enumerate(ALPHABET)}


def clean_text(text: str) -> str:
    """Нижній регістр, заміна ё на е, вилучення всіх символів поза алфавітом."""
    text = text.lower().replace("ё", "е")
    return "".join(ch for ch in text if ch in CHAR_TO_IDX)


def encrypt(plaintext: str, key: str) -> str:
    pt = clean_text(plaintext)
    k = clean_text(key)
    if not k:
        raise ValueError("Ключ має містити хоча б одну літеру російського алфавіту.")
    result = []
    for i, ch in enumerate(pt):
        x = CHAR_TO_IDX[ch]
        shift = CHAR_TO_IDX[k[i % len(k)]]
        result.append(IDX_TO_CHAR[(x + shift) % M])
    return "".join(result)


def decrypt(ciphertext: str, key: str) -> str:
    ct = clean_text(ciphertext)
    k = clean_text(key)
    if not k:
        raise ValueError("Ключ має містити хоча б одну літеру російського алфавіту.")
    result = []
    for i, ch in enumerate(ct):
        y = CHAR_TO_IDX[ch]
        shift = CHAR_TO_IDX[k[i % len(k)]]
        result.append(IDX_TO_CHAR[(y - shift) % M])
    return "".join(result)
