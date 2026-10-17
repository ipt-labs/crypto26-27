import sys
sys.path.insert(0, "../Lab1")
from task2 import bigram_frequencies, read_file

def clean(text):
    return "".join(ch for ch in text if "а" <= ch <= "я")

text = clean(read_file("ishodniki/06_varik_UTF8.txt"))
for bg, c, _ in bigram_frequencies(text, 2)[:5]:
    print(f"{bg}: {c}")