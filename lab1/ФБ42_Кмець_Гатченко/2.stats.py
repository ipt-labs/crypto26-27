import math
from collections import Counter


def analyze_monograms(text: str) -> dict:
    n_chars = len(text)
    if n_chars == 0:
        return {}

    # Підрахунок частот символів
    char_counts = Counter(text)
    char_freqs = {
        char: count / n_chars for char, count in char_counts.items()
    }

    # Обчислення H1
    h1 = -sum(p * math.log2(p) for p in char_freqs.values() if p > 0)

    return {
        "length": n_chars,
        "char_freqs": char_freqs,
        "h1": h1,
    }


def print_top_chars(freq_dict: dict, title: str, top_n: int = 5):

    sorted_items = sorted(
        freq_dict.items(), key=lambda x: x[1], reverse=True
    )[:top_n]
    print(f"--- {title} (Top-{top_n}) ---")
    for item, freq in sorted_items:
        display_item = item.replace(" ", "␣")
        print(f"  '{display_item}': {freq:.6f} ({freq * 100:.2f}%)")


def run_monogram_analysis(file_spaces: str, file_nospaces: str):
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

        res = analyze_monograms(text)

        print(label)
        print(f"Загальна кількість символів: {res['length']}")
        print(f"Ентропія H1 (на символ): {res['h1']:.6f} біт/символ\n")

        print_top_chars(res["char_freqs"], "Символи")
        print("\n")


if __name__ == "__main__":
    run_monogram_analysis("output_with_spaces.txt", "output_without_spaces.txt")