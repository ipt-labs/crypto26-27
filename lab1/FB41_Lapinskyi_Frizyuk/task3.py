import math
import random
from collections import Counter

def calculate_h1(text):
    total = len(text)
    freq = Counter(text)
    entropy = 0.0
    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

if __name__ == "__main__":
    INPUT_FILE = "brothers_karamazov_clean_no_spaces.txt"
    LENGTH = 100000

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        full_text = f.read()
    alphabet = sorted(list(set(full_text)))
    most_common_char = Counter(full_text).most_common(1)[0][0]
    seq_a = full_text[:LENGTH]
    seq_b = most_common_char * LENGTH
    seq_v = "".join(random.choice(alphabet) for _ in range(LENGTH))
    h1_a = calculate_h1(seq_a)
    h1_b = calculate_h1(seq_b)
    h1_v = calculate_h1(seq_v)

    print(f"Довжина послідовностей: {LENGTH} символів")
    print(f"H1(А) [природний текст]       = {h1_a:.4f} біт/символ")
    print(f"H1(Б) [повторення символу]     = {h1_b:.4f} біт/символ")
    print(f"H1(В) [рівноймовірна вибірка]  = {h1_v:.4f} біт/символ")