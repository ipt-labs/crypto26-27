import random
from collections import Counter
from math import log2
from pathlib import Path
 
N = 100_000  # довжина кожної послідовності
 
 
def entropy(counts: Counter) -> float:
    total = sum(counts.values())
    return -sum((c / total) * log2(c / total) for c in counts.values())
 
 
def h1(text: str) -> float:
    return entropy(Counter(text))
 
 
def make_a(source: str, n: int) -> str:
    """А - фрагмент природного тексту (беремо перші n символів)."""
    return source[:n]
 
 
def make_b(symbol: str, n: int) -> str:
    """Б - повторення одного символу."""
    return symbol * n
 
 
def make_v(alphabet: str, n: int) -> str:
    """В - випадкова рівноймовірна послідовність з того самого алфавіту."""
    return "".join(random.choice(alphabet) for _ in range(n))
 
 
def main() -> None:
    random.seed(42)  # для відтворюваності результатів
 
    source = Path("text_no_spaces.txt").read_text(encoding="utf-8")
    alphabet = sorted(set(source))
 
    a = make_a(source, N)
    b = make_b("а", N)
    v = make_v(alphabet, N)
 
    print(f"алфавіт (m={len(alphabet)}): {''.join(alphabet)}")
    print(f"H0 = log2({len(alphabet)}) = {log2(len(alphabet)):.4f}\n")
 
    for name, seq in (("А (природний текст)", a),
                      ("Б (повторення символу)", b),
                      ("В (випадкова рівноймовірна)", v)):
        print(f"{name}: довжина={len(seq)}, різних символів={len(set(seq))}, "
              f"H1={h1(seq):.4f} біт")
 
 
if __name__ == "__main__":
    main()