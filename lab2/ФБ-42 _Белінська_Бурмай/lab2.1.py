from pathlib import Path
from collections import Counter
import csv

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
LETTER_INDEX = {letter: i for i, letter in enumerate(ALPHABET)}
M = len(ALPHABET)

KEYS = ["аб", "мир", "ключ", "книга", "криптография"]


def prepare_text(text):
    text = text.lower().replace("ё", "е")
    return "".join(letter for letter in text if letter in LETTER_INDEX)


def vigenere(text, key, decrypt=False):
    if not key or any(letter not in LETTER_INDEX for letter in key):
        raise ValueError("Ключ має містити лише літери заданого алфавіту.")

    direction = -1 if decrypt else 1
    result = []

    for i, letter in enumerate(text):
        text_number = LETTER_INDEX[letter]
        key_number = LETTER_INDEX[key[i % len(key)]]
        result_number = (text_number + direction * key_number) % M
        result.append(ALPHABET[result_number])

    return "".join(result)


def coincidence_index(text):
    n = len(text)

    if n < 2:
        raise ValueError("Текст має містити щонайменше дві літери.")

    counts = Counter(text)
    numerator = sum(count * (count - 1) for count in counts.values())

    return numerator / (n * (n - 1))


def main():
    base_dir = Path(__file__).resolve().parent
    input_file = base_dir / "lab2.txt"
    output_dir = base_dir / "results"

    if not input_file.is_file():
        raise FileNotFoundError(
            f"Не знайдено файл {input_file}. "
            "Помісти lab2.txt в одну папку з програмою."
        )

    source_text = input_file.read_text(encoding="utf-8-sig")
    plaintext = prepare_text(source_text)

    if len(plaintext) < 2:
        raise ValueError("Після очищення залишилося менше двох літер.")

    output_dir.mkdir(exist_ok=True)

    (output_dir / "plaintext_clean.txt").write_text(
        plaintext, encoding="utf-8"
    )

    plain_ic = coincidence_index(plaintext)
    uniform_ic = 1 / M

    results = [{
        "text": "Відкритий текст",
        "key": "—",
        "length": 0,
        "n": len(plaintext),
        "ic": plain_ic
    }]

    for key in KEYS:
        ciphertext = vigenere(plaintext, key)
        decrypted_text = vigenere(ciphertext, key, decrypt=True)

        if decrypted_text != plaintext:
            raise RuntimeError(f"Помилка розшифрування для ключа {key}.")

        if len(ciphertext) != len(plaintext):
            raise RuntimeError("Довжина тексту змінилася.")

        (output_dir / f"ciphertext_r{len(key)}.txt").write_text(
            ciphertext, encoding="utf-8"
        )

        results.append({
            "text": "Шифртекст",
            "key": key,
            "length": len(key),
            "n": len(ciphertext),
            "ic": coincidence_index(ciphertext)
        })

    lines = [
        "ДОСЛІДЖЕННЯ ШИФРУ ВІЖЕНЕРА",
        "",
        f"Розмір початкового файлу: {input_file.stat().st_size} байтів",
        f"Кількість символів до очищення: {len(source_text)}",
        f"Кількість літер після очищення: {len(plaintext)}",
        f"Розмір алфавіту: {M}",
        f"Орієнтир рівномірного розподілу: 1/32 = {uniform_ic:.9f}",
        "",
        f"{'Текст':<20} {'Ключ':<15} {'r':>3} {'n':>6} {'Індекс':>14}",
        "-" * 65
    ]

    for row in results:
        r = str(row["length"]) if row["length"] else "—"
        lines.append(
            f"{row['text']:<20} "
            f"{row['key']:<15} "
            f"{r:>3} "
            f"{row['n']:>6} "
            f"{row['ic']:>14.9f}"
        )

    best = min(
        results[1:],
        key=lambda row: abs(row["ic"] - uniform_ic)
    )

    monotonic = all(
        results[i]["ic"] >= results[i + 1]["ic"]
        for i in range(1, len(results) - 1)
    )

    lines.extend([
        "",
        "ПОРІВНЯННЯ З ВІДКРИТИМ ТЕКСТОМ"
    ])

    for row in results[1:]:
        difference = row["ic"] - plain_ic
        lines.append(
            f"Ключ «{row['key']}», r={row['length']}: "
            f"зміна індексу {difference:+.9f}."
        )


    report = "\n".join(lines)
    print(report)

    (output_dir / "results.txt").write_text(
        report, encoding="utf-8"
    )

    with (output_dir / "indices.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([
            "Текст", "Ключ", "Довжина ключа",
            "Кількість літер", "Індекс відповідності"
        ])

        for row in results:
            writer.writerow([
                row["text"],
                row["key"],
                row["length"] or "—",
                row["n"],
                f"{row['ic']:.9f}"
            ])

    print(f"\nФайли збережено в: {output_dir}")


if __name__ == "__main__":
    main()