import math
from collections import Counter


normalized = "normalized.txt"
b_file = "B.txt"
c_file = "C.txt"


def symbol_frequencies(text):

    return Counter(text)


def calculate_h1(text):

    frequencies = symbol_frequencies(text)
    total = len(text)
    h1 = 0

    for count in frequencies.values():
        p = count / total
        h1 -= p * math.log2(p)

    return h1


def print_statistics(text, name):

    print(name)

    h1 = calculate_h1(text)
    print(f"H1 = {h1:.6f} біт")


with open(normalized, "r", encoding="utf-8") as file:
    natural_text = file.read()


with open(b_file, "r", encoding="utf-8") as file:
    b_text = file.read()


with open(c_file, "r", encoding="utf-8") as file:
    c_text = file.read()


print_statistics(
    natural_text,
    "\nПриродний текст"
)


print_statistics(
    b_text,
    "\nПовторення одного символу"
)


print_statistics(
    c_text,
    "\nСимволи з однаковою ймовірністю"
)