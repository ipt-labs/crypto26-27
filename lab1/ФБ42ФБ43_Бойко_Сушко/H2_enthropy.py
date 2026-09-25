import math
from collections import Counter

with open('Task4_periodic.txt', 'r', encoding='utf-8') as f:
    text = f.read()


bigrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]
total_bigrams = len(bigrams)

bigram_counts = Counter(bigrams)

h_bigram = 0.0

for count in bigram_counts.values():
    p_i = count / total_bigrams
    h_bigram -= p_i * math.log2(p_i)

h2 = h_bigram / 2

print(f"Ентропія H2: {h2:.4f} біт")

