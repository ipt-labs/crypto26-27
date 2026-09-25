import random
from collections import Counter
from math import log2
 
N = 100_000  # довжина кожної послідовності (парна, щоб symbols were 50/50)
ALPHABET = "ab"  # умовний двосимвольний алфавіт для наочності
 
 
def entropy(counts: Counter) -> float:
    total = sum(counts.values())
    return -sum((c / total) * log2(c / total) for c in counts.values())
 
 
def h1(text: str) -> float:
    return entropy(Counter(text))
 
 
def bigram_counts(text: str, overlapping: bool) -> Counter:
    step = 1 if overlapping else 2
    return Counter(text[i:i + 2] for i in range(0, len(text) - 1, step))
 
 
def h2(text: str, overlapping: bool) -> float:
    return entropy(bigram_counts(text, overlapping)) / 2
 
 
def make_g(alphabet: str, n: int) -> str:
    """Г - символи у випадковому порядку, частоти рівні (по n/len(alphabet))."""
    symbols = list(alphabet) * (n // len(alphabet))
    random.shuffle(symbols)
    return "".join(symbols)
 
 
def make_d(alphabet: str, n: int) -> str:
    """Д - періодична структура: символи алфавіту по черзі, наприклад abab..."""
    return (alphabet * (n // len(alphabet) + 1))[:n]
 
 
def main() -> None:
    random.seed(42)
 
    g = make_g(ALPHABET, N)
    d = make_d(ALPHABET, N)
 
    for name, seq in (("Г (випадковий порядок)", g),
                      ("Д (періодична структура)", d)):
        print(f"\n=== {name} ===")
        print(f"довжина={len(seq)}, частоти: {dict(Counter(seq))}")
        print(f"H1 = {h1(seq):.4f} біт")
        for overlapping, label in ((True, "перетинні"), (False, "неперетинні")):
            bc = bigram_counts(seq, overlapping)
            print(f"H2 ({label}) = {h2(seq, overlapping):.4f} біт "
                  f"[біграми: {dict(bc.most_common())}]")
 
 
if __name__ == "__main__":
    main()