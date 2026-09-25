import math
from collections import Counter

with open('Task4_random.txt', 'r', encoding='utf-8') as f:
    text = f.read()

frequencies = Counter(text)
total_chars = len(text)

h1 = 0.0

for key in sorted(frequencies.keys()):
    p_i = frequencies[key] / total_chars
    
    h1 -= p_i * math.log2(p_i)
    
print(f"Ентропія H1: {h1:.4f} біт на символ")