import math
from collections import Counter

normalized = "normalized.txt"
no_spaces = "withoutSpaces.txt"

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

    frequencies = symbol_frequencies(text)
    total = len(text)

    print("\nТоп-5 символів:")

    for symbol, count in frequencies.most_common(5):

        if symbol == " ":
            symbol = "space"

        probability = count / total

        print(f"{symbol}: {count}, p = {probability:.6f}")

    h1 = calculate_h1(text)

    print(f"\nH1 = {h1:.6f} біт")


with open(normalized, "r", encoding="utf-8") as file:
    normalized_text = file.read()

with open(no_spaces, "r", encoding="utf-8") as file:
    text_without_spaces = file.read()


print_statistics(
    normalized_text,
    "\nNormalized"
)


print_statistics(
    text_without_spaces,
    "\nWithoutSpaces"
)