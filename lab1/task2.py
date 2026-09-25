import math
from collections import Counter

def calculate_entropy(freq_dict, total_count, n):
    entropy = 0.0
    for count in freq_dict.values():
        p = count / total_count
        entropy -= p * math.log2(p)
    return entropy / n

def get_ngrams(text, n, step):
    ngrams = []
    for i in range(0, len(text) - n + 1, step):
        ngrams.append(text[i:i + n])
    return ngrams

def analyze_text(text, label):
    print(f"\n{'=' * 50}")
    print(f"АНАЛІЗ ТЕКСТУ: {label}")
    print(f"{'=' * 50}")
    chars = list(text)
    total_chars = len(chars)
    char_freq = Counter(chars)
    h1 = calculate_entropy(char_freq, total_chars, 1)

    print(f"\n[ H1 ] Ентропія окремих символів: {h1:.5f} біт/символ")
    print("Топ-5 символів:")
    for k, v in char_freq.most_common(5):
        print(f"  '{k}': {v} разів (p = {v / total_chars:.4f})")

    bigrams_overlap = get_ngrams(text, 2, 1)
    total_bo = len(bigrams_overlap)
    bo_freq = Counter(bigrams_overlap)
    h2_overlap = calculate_entropy(bo_freq, total_bo, 2)

    print(f"\n[ H2 ] Біграми ЩО ПЕРЕТИНАЮТЬСЯ (зміщення 1): {h2_overlap:.5f} біт/символ")
    print(f"Загальна кількість таких біграм: {total_bo}")
    print("Топ-5 біграм:")
    for k, v in bo_freq.most_common(5):
        print(f"  '{k}': {v} разів (p = {v / total_bo:.4f})")

    bigrams_no_overlap = get_ngrams(text, 2, 2)
    total_bno = len(bigrams_no_overlap)
    bno_freq = Counter(bigrams_no_overlap)
    h2_no_overlap = calculate_entropy(bno_freq, total_bno, 2)

    print(f"\n[ H2 ] Біграми ЩО НЕ ПЕРЕТИНАЮТЬСЯ (зміщення 2): {h2_no_overlap:.5f} біт/символ")
    print(f"Загальна кількість таких біграм: {total_bno}")
    print("Топ-5 біграм:")
    for k, v in bno_freq.most_common(5):
        print(f"  '{k}': {v} разів (p = {v / total_bno:.4f})")


if __name__ == "__main__":
    FILE_WITH_SPACES = "brothers_karamazov_clean_with_spaces.txt"
    FILE_NO_SPACES = "brothers_karamazov_clean_no_spaces.txt"

    try:
        with open(FILE_WITH_SPACES, "r", encoding="utf-8") as f:
            text_with_spaces = f.read()
        with open(FILE_NO_SPACES, "r", encoding="utf-8") as f:
            text_no_spaces = f.read()
        analyze_text(text_with_spaces, "З ПРОБІЛАМИ")
        analyze_text(text_no_spaces, "БЕЗ ПРОБІЛІВ")
    except FileNotFoundError:
        print("Помилка: Файли для аналізу не знайдені. Спершу виконайте Завдання 1.")