from collections import Counter
from math import log2

LETTERS = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_WITH_SPACE = LETTERS + " "


def h0(alphabet):
    return log2(len(alphabet))


def char_freqs(text):
    return Counter(text)


def bigram_freqs(text, overlapping=True):
    step = 1 if overlapping else 2
    return Counter(text[i:i + 2] for i in range(0, len(text) - 1, step))


def entropy(counts):
    total = sum(counts.values())
    if total == 0:
        return 0.0
    h = -sum((c / total) * log2(c / total) for c in counts.values())
    return h + 0.0


def h1(text):
    return entropy(char_freqs(text))


def h2(text, overlapping=True):
    return entropy(bigram_freqs(text, overlapping)) / 2


def redundancy(h, alphabet):
    return 1 - h / h0(alphabet)


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def top_n(counts, n=5):
    total = sum(counts.values())
    return [(item, cnt, cnt / total) for item, cnt in counts.most_common(n)]