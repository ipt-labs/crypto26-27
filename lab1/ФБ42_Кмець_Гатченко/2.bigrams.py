import math
from collections import Counter


def analyze_bigrams(text: str) -> dict:

    n_chars = len(text)
    if n_chars < 2:
        return {}

    overlap_bigrams = [text[i : i + 2] for i in range(n_chars - 1)]
    n_overlap = len(overlap_bigrams)
    overlap_counts = Counter(overlap_bigrams)
    overlap_freqs = (
        {bg: count / n_overlap for bg, count in overlap_counts.items()}
        if n_overlap > 0
        else {}
    )

    h2_overlap = (
        -0.5
        * sum(p * math.log2(p) for p in overlap_freqs.values() if p > 0)
        if overlap_freqs
        else 0.0
    )

    non_overlap_bigrams = [
        text[i : i + 2]
        for i in range(0, n_chars - 1, 2)
        if len(text[i : i + 2]) == 2
    ]
    n_non_overlap = len(non_overlap_bigrams)
    non_overlap_counts = Counter(non_overlap_bigrams)
    non_overlap_freqs = (
        {bg: count / n_non_overlap for bg, count in non_overlap_counts.items()}
        if n_non_overlap > 0
        else {}
    )

    h2_non_overlap = (
        -0.5
        * sum(p * math.log2(p) for p in non_overlap_freqs.values() if p > 0)
        if non_overlap_freqs
        else 0.0
    )

    return {
        "length": n_chars,
        "overlap_freqs": overlap_freqs,
        "h2_overlap": h2_overlap,
        "n_overlap": n_overlap,
        "non_overlap_freqs": non_overlap_freqs,
        "h2_non_overlap": h2_non_overlap,
        "n_non_overlap": n_non_overlap,
    }


def print_top_bigrams(freq_dict: dict, title: str, top_n: int = 5):

    sorted_items = sorted(
        freq_dict.items(), key=lambda x: x[1], reverse=True
    )[:top_n]
    print(f"--- {title} (Top-{top_n}) ---")
    for item, freq in sorted_items:
        display_item = item.replace(" ", "␣")
        print(f"  '{display_item}': {freq:.6f} ({freq * 100:.2f}%)")


def run_bigram_analysis(file_spaces: str, file_nospaces: str):
    files = [
        ("Текст З ПРОБІЛАМИ", file_spaces),
        ("Текст БЕЗ ПРОБІЛІВ", file_nospaces),
    ]

    for label, filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read().strip()
        except FileNotFoundError:
            print(f"Помилка: Файл '{filepath}' не знайдено.\n")
            continue

        res = analyze_bigrams(text)


        print(label)

        print(f"Загальна кількість символів у тексті: {res['length']}\n")

        print(
            f"Біграми З ПЕРЕТИНОМ | Всього біграм: {res['n_overlap']}"
        )
        print(
            f"Ентропія H2 (з перетином): {res['h2_overlap']:.6f} біт/символ"
        )
        print_top_bigrams(res["overlap_freqs"], "Біграми з перетином")
        print()

        print(
            f"Біграми БЕЗ ПЕРЕТИНУ | Всього біграм: {res['n_non_overlap']}"
        )
        print(
            f"Ентропія H2 (без перетину): {res['h2_non_overlap']:.6f} біт/символ"
        )
        print_top_bigrams(res["non_overlap_freqs"], "Біграми без перетину")
        print("\n")


if __name__ == "__main__":
    run_bigram_analysis("output_with_spaces.txt", "output_without_spaces.txt")