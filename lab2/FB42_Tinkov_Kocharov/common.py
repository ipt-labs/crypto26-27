from collections import Counter

ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
M = len(ALPHABET)
IDX = {c: i for i, c in enumerate(ALPHABET)}

RU_FREQ = {
    'а': 0.07707, 'б': 0.01812, 'в': 0.04658, 'г': 0.01928,
    'д': 0.03176, 'е': 0.08916, 'ж': 0.01115, 'з': 0.01537,
    'и': 0.06769, 'й': 0.01009, 'к': 0.03265, 'л': 0.04510,
    'м': 0.03332, 'н': 0.06152, 'о': 0.11388, 'п': 0.02658,
    'р': 0.04064, 'с': 0.05298, 'т': 0.06588, 'у': 0.02899,
    'ф': 0.00171, 'х': 0.00770, 'ц': 0.00339, 'ч': 0.01797,
    'ш': 0.00969, 'щ': 0.00286, 'ъ': 0.00024, 'ы': 0.01680,
    'ь': 0.02069, 'э': 0.00363, 'ю': 0.00683, 'я': 0.02071,
}


def clean(text):
    text = text.lower().replace('ё', 'е')
    return ''.join(c for c in text if c in IDX)


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def encrypt(text, key):
    k = [IDX[c] for c in key]
    return ''.join(ALPHABET[(IDX[c] + k[i % len(k)]) % M] for i, c in enumerate(text))


def decrypt(text, key):
    k = [IDX[c] for c in key]
    return ''.join(ALPHABET[(IDX[c] - k[i % len(k)]) % M] for i, c in enumerate(text))


def index_of_coincidence(text):
    n = len(text)
    if n < 2:
        return 0.0
    return sum(v * (v - 1) for v in Counter(text).values()) / (n * (n - 1))


def frequencies(text):
    cnt = Counter(text)
    return {c: cnt.get(c, 0) / len(text) for c in ALPHABET}


def theoretical_ic():
    return sum(p * p for p in RU_FREQ.values())


def blocks(text, r):
    return [text[i::r] for i in range(r)]