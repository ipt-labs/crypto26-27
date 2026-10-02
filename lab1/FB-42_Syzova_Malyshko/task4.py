import math
import random
from collections import Counter

def calc_entropy(frequencies, total_count, n_gram_length):
    entropy = 0
    for count in frequencies.values():
        p = count / total_count
        entropy -= p * math.log2(p)
    return entropy / n_gram_length

def analyze_seq(text):
    h1 = calc_entropy(Counter(text), len(text), 1)
    bigrams_cross = [text[i:i+2] for i in range(0, len(text)-1, 1)]
    h2_cross = calc_entropy(Counter(bigrams_cross), len(bigrams_cross), 2)  
    bigrams_nocross = [text[i:i+2] for i in range(0, len(text)-1, 2)]

    if len(bigrams_nocross[-1]) == 1:
        bigrams_nocross = bigrams_nocross[:-1]
    h2_nocross = calc_entropy(Counter(bigrams_nocross), len(bigrams_nocross), 2)
    
    return h1, h2_cross, h2_nocross

if __name__ == "__main__":
    length = 10000 
    seq_D = ('аб' * (length // 2))  
    seq_G_list = list(seq_D)
    random.shuffle(seq_G_list)
    seq_G = ''.join(seq_G_list)
    
    h1_D, h2_c_D, h2_n_D = analyze_seq(seq_D)
    h1_G, h2_c_G, h2_n_G = analyze_seq(seq_G)
    
    print("Послідовність Д (періодична)")
    print(f"H1: {h1_D:.5f}")
    print(f"H2 (перетинаються): {h2_c_D:.5f}")
    print(f"H2 (не перетинаються): {h2_n_D:.5f}\n")

    print("Послідовність Г (випадкова)")
    print(f"H1: {h1_G:.5f}")
    print(f"H2 (перетинаються): {h2_c_G:.5f}")
    print(f"H2 (не перетинаються): {h2_n_G:.5f}")