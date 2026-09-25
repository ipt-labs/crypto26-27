import csv
from collections import Counter
from math import log2
from pathlib import Path
 
OUT_DIR = Path("results")
 
 
def letter_counts(text: str) -> Counter:
    return Counter(text)
 
 
def bigram_counts(text: str, overlapping: bool) -> Counter:
    """Біграми зі зсувом на 1 символ (перетинні) або на 2 (неперетинні)."""
    step = 1 if overlapping else 2
    return Counter(text[i:i + 2] for i in range(0, len(text) - 1, step))
 
 
def entropy(counts: Counter) -> float:
    """H = -sum(p * log2 p)."""
    total = sum(counts.values())
    return -sum((c / total) * log2(c / total) for c in counts.values())
 
 
def h1(text: str) -> float:
    return entropy(letter_counts(text))
 
 
def h2(text: str, overlapping: bool) -> float:
    """Ентропія біграми, поділена на 2 - потрібна ентропія НА СИМВОЛ."""
    return entropy(bigram_counts(text, overlapping)) / 2
 
 
def top(counts: Counter, n: int = 5) -> str:
    total = sum(counts.values())
    return ", ".join(f"'{k}' {v / total:.4f}" for k, v in counts.most_common(n))
 
 
def save_table(path: Path, counts: Counter) -> None:
    total = sum(counts.values())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["символ", "кількість", "частота"])
        for k, v in counts.most_common():
            w.writerow([k, v, f"{v / total:.6f}"])
 
 
def analyze(name: str, text: str) -> None:
    print(f"\n=== {name} ===")
    print(f"довжина: {len(text)}, різних символів: {len(set(text))}")
 
    lc = letter_counts(text)
    print(f"H1 = {entropy(lc):.4f} біт")
    print(f"  топ-5 символів: {top(lc)}")
    save_table(OUT_DIR / f"{name}_letters.csv", lc)
 
    for overlapping, label, tag in ((True, "перетинні", "overlap"),
                                    (False, "неперетинні", "nonoverlap")):
        bc = bigram_counts(text, overlapping)
        print(f"H2 ({label}) = {h2(text, overlapping):.4f} біт "
              f"[біграм: {sum(bc.values())}, різних: {len(bc)}]")
        print(f"  топ-5 біграм: {top(bc)}")
        save_table(OUT_DIR / f"{name}_bigrams_{tag}.csv", bc)
 
 
def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    for name, fname in (("with_spaces", "text_with_spaces.txt"),
                        ("no_spaces", "text_no_spaces.txt")):
        text = Path(fname).read_text(encoding="utf-8")
        analyze(name, text)
 
 
if __name__ == "__main__":
    main()