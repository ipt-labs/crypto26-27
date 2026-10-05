import math
from collections import Counter


normalized = "normalized.txt"
no_spaces = "withoutSpaces.txt"


def bigram_frequencies(text, step):

    bigrams = []

    for i in range(0, len(text) - 1, step):

        bigrams.append(text[i:i + 2])

    return Counter(bigrams)


def calculate_h2(text, step):

    frequencies = bigram_frequencies(text, step)

    total = sum(frequencies.values())

    h2 = 0

    for count in frequencies.values():

        p = count / total

        h2 -= p * math.log2(p)

    return h2 / 2


def print_statistics(text, name):

    print(name)

    # Біграми, що перетинаються
    
    overlap = bigram_frequencies(text, 1)
    print("\nТоп-5 біграм, що перетинаються:")
    total = sum(overlap.values())

    for bigram, count in overlap.most_common(5):
        probability = count / total
        display_bigram = bigram.replace(" ", "[space]")
        print(f"{display_bigram}: {count}, p = {probability:.6f}")

    h2_overlap = calculate_h2(text, 1)

    print(
        f"\nH2 = "
        f"{h2_overlap:.6f} біт"
    )

    # Біграми, що не перетинаються

    non_overlap = bigram_frequencies(text, 2)

    print("\nТоп-5 біграм, що не перетинаються:")

    total = sum(non_overlap.values())

    for bigram, count in non_overlap.most_common(5):

        probability = count / total

        display_bigram = bigram.replace(" ", "[space]")

        print(f"{display_bigram}: {count}, p = {probability:.6f}")

    h2_non_overlap = calculate_h2(text, 2)

    print(
        f"\nH2 = "
        f"{h2_non_overlap:.6f} біт"
    )


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