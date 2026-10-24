from pathlib import Path
from collections import Counter

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"



def coincidence_index(text):
    n = len(text)
    counts = Counter(text)
    return sum(count * (count - 1) for count in counts.values()) / (n * (n - 1))


if __name__ == "__main__":
    input_file1 = "output_without_spaces.txt"
    input_file2 = "variant5.txt"
    with open(input_file1, 'r', encoding='utf-8') as f:
                   reference = f.read()
    with open(input_file2, 'r', encoding='utf-8') as f:
                   text = f.read()
    counts = Counter(reference)
    expected_index = sum((count / len(reference)) ** 2 for count in counts.values())

    print(f"Текст з КП1: {len(reference)} літер")
    print(f"Сума квадратів частот: {expected_index:.6f}")
    print(f"Рівноймовірний алфавіт: {1 / 32:.6f}")
    print(f"Варіант 5: {len(text)} літер, I = {coincidence_index(text):.6f}")
    print()
    results = []
    for r in range(2, 31):
        indices = []
        for j in range(r):
            block = text[j::r]
            indices.append(coincidence_index(block))
        average = sum(indices) / r
        results.append((r, average))
    print(" r   Середній I       r   Середній I")
    for i in range(15):
        r, average = results[i]
        line = f"{r:2}   {average:.6f}"
        if i + 15 < len(results):
            other_r, other_average = results[i + 15]
            line += f"        {other_r:2}   {other_average:.6f}"
        print(line)
