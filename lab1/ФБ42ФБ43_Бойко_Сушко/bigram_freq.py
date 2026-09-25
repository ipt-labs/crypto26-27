from collections import Counter

with open('Crypto_normalized_no_spaces.txt', 'r', encoding='utf-8') as f:
    text = f.read()

bigrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]

bigram_counts = Counter(bigrams)

for key in bigram_counts.most_common(5):
    print(f"'{key[0]}': {key[1]/len(bigrams):.4f}")