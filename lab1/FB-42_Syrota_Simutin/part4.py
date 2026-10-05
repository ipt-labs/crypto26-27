import math
from collections import Counter


random = "random.txt"
order = "order.txt"


def symbol_frequencies(text):

    return Counter(text)


def bigram_frequencies(text, step):

    bigrams = []
    for i in range(0, len(text) - 1, step):
        bigrams.append(text[i:i + 2])

    return Counter(bigrams)


def calculate_h1(text):

    frequencies = symbol_frequencies(text)
    total = len(text)
    h1 = 0

    for count in frequencies.values():

        p = count / total
        h1 -= p * math.log2(p)

    return h1


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
 
    h1 = calculate_h1(text) 
    print(f"H1 = {h1:.6f} біт") 
 
    # Біграми, що перетинаються 
 
    h2_overlap = calculate_h2(text, 1) 
    print(f"\nH2 (біграми, що перетинаються) = {h2_overlap:.6f} біт") 
 
    # Біграми, що не перетинаються 
 
    h2_non_overlap = calculate_h2(text, 2) 
    print(f"H2 (біграми, що не перетинаються) = {h2_non_overlap:.6f} біт") 
 
 
with open(random, "r", encoding="utf-8") as file: 
 
    random_text = file.read() 
 
 
with open(order, "r", encoding="utf-8") as file: 
 
    order_text = file.read() 
 
 
print_statistics( 
    random_text, 
    "\nRandom" 
) 
 
 
print_statistics( 
    order_text, 
    "\nOrder" 
)