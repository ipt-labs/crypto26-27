from collections import Counter

ALPHABETS = ('абвгдежзийклмнопрстуфхцчшщьыэюя',
             'абвгдежзийклмнопрстуфхцчшщыьэюя')
M = 31
M2 = M * M

FREQ_LETTERS = ('о', 'а', 'е')
RARE_LETTERS = ('ф', 'щ', 'ь')
LANG_BIGRAMS = ('ст', 'но', 'то', 'на', 'ен')


def read(path, encoding='utf-8'):
    with open(path, 'rb') as f:
        return f.read().decode(encoding)


def clean(text, alpha=ALPHABETS[0]):
    text = text.lower().replace('ё', 'е').replace('ъ', 'ь')
    return ''.join(c for c in text if c in alpha)


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def inverse(a, n):
    g, x, _ = egcd(a % n, n)
    if g != 1:
        return None
    return x % n


def solve_congruence(a, b, n):
    a, b = a % n, b % n
    g, x, _ = egcd(a, n)
    if b % g != 0:
        return []
    x0 = (x * (b // g)) % (n // g)
    return sorted((x0 + i * (n // g)) % n for i in range(g))


def bigram_to_num(bg, alpha):
    return alpha.index(bg[0]) * M + alpha.index(bg[1])


def num_to_bigram(x, alpha):
    return alpha[x // M] + alpha[x % M]


def bigrams(text):
    return [text[i:i + 2] for i in range(0, len(text) - 1, 2)]


def decrypt(text, a, b, alpha):
    a_inv = inverse(a, M2)
    if a_inv is None:
        return None
    out = []
    for bg in bigrams(text):
        x = (a_inv * (bigram_to_num(bg, alpha) - b)) % M2
        out.append(num_to_bigram(x, alpha))
    return ''.join(out)


def letter_freq(text, alpha):
    cnt = Counter(text)
    return {c: cnt.get(c, 0) / len(text) for c in alpha}