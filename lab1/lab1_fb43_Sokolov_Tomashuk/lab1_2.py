from collections import Counter
import math
import os
import sys

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def calculate_entropy_and_frequencies(text):
    total = len(text)
    counts = Counter(text)
    h1 = 0.0

    freqs = {}
    for char, count in counts.items():
        p = count / total
        freqs[char] = p
        h1 -= p * math.log2(p)

    return h1, freqs, counts


def calculate_bigram_entropy(text, step=1):
    bigrams = [text[i : i + 2] for i in range(0, len(text) - 1, step)]
    total = len(bigrams)
    counts = Counter(bigrams)

    h_pair = 0.0
    freqs = {}
    for bg, count in counts.items():
        p = count / total
        freqs[bg] = p
        h_pair -= p * math.log2(p)

    h2 = h_pair / 2.0
    return h2, freqs, counts, total


def analyze_file(filename, has_spaces_label):
    file_path = os.path.join(SCRIPT_DIR, filename)

    if not os.path.exists(file_path):
        print(f"\n[ПОМИЛКА] Файл не знайдено: {file_path}")
        print(
            f"Переконайтеся, що файл '{filename}' лежить саме в папці '{SCRIPT_DIR}'."
        )
        return

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"\n{'='*60}")
    print(f"АНАЛІЗ ТЕКСТУ: {has_spaces_label.upper()}")
    print(f"Загальна довжина: {len(text)} символів")
    print(f"{'='*60}")

    h1, char_freqs, char_counts = calculate_entropy_and_frequencies(text)
    m = len(char_counts)
    h0 = math.log2(m)
    print(f"\nКількість унікальних символів (m): {m}")
    print(f"H0 (максимальна ентропія = log2(m)): {h0:.4f} біт/символ")
    print(f"H1 (ентропія символів):              {h1:.4f} біт/символ")

    print("\n--- ТОП-5 СИМВОЛІВ ---")
    for ch, cnt in char_counts.most_common(5):
        display_ch = "' '" if ch == " " else f"'{ch}'"
        print(
            f"  Символ {display_ch:>3}: {cnt:>8} разів | Ймовірність p = {char_freqs[ch]:.5f}"
        )

    h2_overlap, bg_freqs_ov, bg_counts_ov, total_ov = calculate_bigram_entropy(
        text, step=1
    )
    print(f"\nБіграми З ПЕРЕТИНОМ (крок 1):")
    print(f"  Всього біграм:        {total_ov}")
    print(f"  Унікальних біграм:    {len(bg_counts_ov)}")
    print(f"  H2 (з перетином):     {h2_overlap:.4f} біт/символ")

    print("  --- Топ-5 біграм (з перетином) ---")
    for bg, cnt in bg_counts_ov.most_common(5):
        print(f"    Біграма '{bg}': {cnt:>7} | p = {bg_freqs_ov[bg]:.5f}")

    h2_no_overlap, bg_freqs_no, bg_counts_no, total_no = (
        calculate_bigram_entropy(text, step=2)
    )
    print(f"\nБіграми БЕЗ ПЕРЕТИНУ (крок 2):")
    print(f"  Всього біграм:        {total_no}")
    print(f"  Унікальних біграм:    {len(bg_counts_no)}")
    print(f"  H2 (без перетину):    {h2_no_overlap:.4f} біт/символ")

    print("  --- Топ-5 біграм (без перетину) ---")
    for bg, cnt in bg_counts_no.most_common(5):
        print(f"    Біграма '{bg}': {cnt:>7} | p = {bg_freqs_no[bg]:.5f}")

    csv_char_file = os.path.join(
        SCRIPT_DIR, f"freqs_chars_{has_spaces_label}.csv"
    )
    with open(csv_char_file, "w", encoding="utf-8") as f_out:
        f_out.write("Символ,Кількість,Частота (p)\n")
        for ch, cnt in char_counts.most_common():
            display_ch = "ПРОБІЛ" if ch == " " else ch
            f_out.write(f'"{display_ch}",{cnt},{char_freqs[ch]:.6f}\n')

    csv_bg_file = os.path.join(
        SCRIPT_DIR, f"freqs_bigrams_overlap_{has_spaces_label}.csv"
    )
    with open(csv_bg_file, "w", encoding="utf-8") as f_out:
        f_out.write("Біграма,Кількість,Частота (p)\n")
        for bg, cnt in bg_counts_ov.most_common():
            f_out.write(f'"{bg}",{cnt},{bg_freqs_ov[bg]:.6f}\n')


if __name__ == "__main__":
    analyze_file("text_with_spaces.txt", "with_spaces")
    analyze_file("text_without_spaces.txt", "without_spaces")