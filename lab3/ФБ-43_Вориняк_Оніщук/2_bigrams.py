import sys
from collections import Counter


def read(path):
    return "".join(open(path, encoding="utf-8").read().split())


def bigrams(t, step):
    return Counter(a + b for a, b in zip(t[::step], t[1::step]))


if __name__ == "__main__":
    text = read(sys.argv[1])
    for bg, k in bigrams(text, 2).most_common(5):
        print(bg, k, round(k / (len(text) // 2), 5))
