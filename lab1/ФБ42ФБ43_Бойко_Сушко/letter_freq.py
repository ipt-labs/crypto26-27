from collections import Counter

with open('Crypto_normalized_no_spaces.txt', 'r', encoding='utf-8') as f:
    text = f.read()
frequencies = Counter(text)

for key in frequencies.most_common(5):
    print(f"'{key[0]}': {key[1]/len(text):.4f}")