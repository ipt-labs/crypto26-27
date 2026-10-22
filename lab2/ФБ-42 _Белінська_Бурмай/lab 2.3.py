from pathlib import Path
from collections import Counter
import argparse
import csv
import json

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
INDEX = {c: i for i, c in enumerate(ALPHABET)}
M = len(ALPHABET)


def read_ciphertext(path):
    raw = path.read_text(encoding="utf-8-sig").lower()
    invalid = set(raw) - set(ALPHABET) - set(" \t\r\n\ufeff")
    if invalid:
        raise ValueError(f"Сторонні символи в шифртексті: {sorted(invalid)}")
    return "".join(c for c in raw if c in INDEX)


def transform(text, key, decrypt=False):
    if not key or set(key) - set(ALPHABET):
        raise ValueError("Ключ має бути непорожнім і належати заданому алфавіту.")
    direction = -1 if decrypt else 1
    return "".join(ALPHABET[(INDEX[c] + direction * INDEX[key[i % len(key)]]) % M]
                   for i, c in enumerate(text))


def coincidence_index(text):
    n = len(text)
    return sum(v * (v - 1) for v in Counter(text).values()) / (n * (n - 1))


def minimum_period(key):
    for p in range(1, len(key) + 1):
        if len(key) % p == 0 and key == key[:p] * (len(key) // p):
            return p


def load_reference(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict) or set(data) != set(ALPHABET):
        raise ValueError("JSON має містити всі 32 літери алфавіту як ключі.")
    weights = {c: float(data[c]) for c in ALPHABET}
    if any(not 0 < value < float("inf") for value in weights.values()):
        raise ValueError("Усі частоти мають бути скінченними та додатними.")
    total = sum(weights.values())
    if not 0 < total < float("inf"):
        raise ValueError("Некоректна сума частот.")
    probabilities = {c: v / total for c, v in weights.items()}
    label = (f"Повна статистика 32 літер без пробілів із {path.name}. "
             "У наданому файлі КП1 частоти отримано з 746137 літер; ё замінено на е. "
             "Використано всі частоти без згладжування.")
    return probabilities, label


def recover_key(ciphertext, period, probabilities):
    common_plain = sorted(ALPHABET, key=lambda c: (-probabilities[c], INDEX[c]))
    results = []
    for j in range(period):
        block = ciphertext[j::period]
        counts = Counter(block)
        top = sorted(ALPHABET, key=lambda c: (-counts[c], INDEX[c]))[:5]
        y = top[0]
        candidates = []
        for x in common_plain:
            shift = (INDEX[y] - INDEX[x]) % M
            score = sum(
                (counts[ALPHABET[(INDEX[t] + shift) % M]] - len(block) * probabilities[t]) ** 2
                / (len(block) * probabilities[t])
                for t in ALPHABET
            )
            candidates.append({"plain_mode": x, "key": ALPHABET[shift], "shift": shift, "chi2": score})
        candidates.sort(key=lambda item: (item["chi2"], item["shift"]))
        best = candidates[0]
        results.append({"position": j + 1, "n": len(block), "cipher_mode": y,
                        "mode_count": counts[y], "mode_frequency": counts[y] / len(block),
                        "initial_key": ALPHABET[(INDEX[y] - INDEX['о']) % M],
                        "plain_mode": best["plain_mode"], "key": best["key"],
                        "shift": best["shift"], "chi2": best["chi2"],
                        "top5": ", ".join(f"{c}:{counts[c]}" for c in top),
                        "candidates": candidates})
    return "".join(row["key"] for row in results), results, common_plain


def main(cipher_path, reference_path, period, output_dir):
    ciphertext = read_ciphertext(cipher_path)
    if period < 1 or len(ciphertext) < 2 * period:
        raise ValueError("Некоректний період або недостатня довжина шифртексту.")
    probabilities, reference_label = load_reference(reference_path)
    key, rows, common_plain = recover_key(ciphertext, period, probabilities)
    plaintext = transform(ciphertext, key, decrypt=True)
    initial_key = "".join(row["initial_key"] for row in rows)
    initial_plaintext = transform(ciphertext, initial_key, decrypt=True)
    roundtrip = transform(plaintext, key) == ciphertext
    if not roundtrip:
        raise AssertionError("Повторне шифрування не збігається із вхідним шифртекстом.")
    changed = [row["position"] for row in rows if row["key"] != row["initial_key"]]

    lines = [
        "КП2. ЗАВДАННЯ 3. ВІДНОВЛЕННЯ КЛЮЧА ТА ВІДКРИТОГО ТЕКСТУ",
        f"Вхідний файл: {cipher_path.name}; літер: {len(ciphertext)}; період із завдання 2: {period}.",
        "", "ДЖЕРЕЛО СТАТИСТИКИ КП1", reference_label,
        f"Мовний орієнтир sum(p_t^2)={sum(p*p for p in probabilities.values()):.12f}.",
        "", f"Початковий ключ за припущенням x*=о: {initial_key}",
        f"Уточнений ключ: {key}",
        f"Уточнено позиції (від 1): {', '.join(map(str, changed)) or 'немає'}.",
        "", "ПРОМІЖНІ РЕЗУЛЬТАТИ",
        f"{'№':>2} {'L':>3} {'y*':>2} {'N(y*)':>5} {'f(y*)':>9} {'x*':>2} {'k':>2} {'Зсув':>4} {'chi2':>9}",
        "-" * 59
    ]
    for row in rows:
        lines.append(f"{row['position']:>2} {row['n']:>3} {row['cipher_mode']:>2} "
                     f"{row['mode_count']:>5} {row['mode_frequency']:>9.6f} "
                     f"{row['plain_mode']:>2} {row['key']:>2} {row['shift']:>4} {row['chi2']:>9.3f}")
    lines.extend(["", "ЧАСТОТИ ТА АЛЬТЕРНАТИВНІ ВІДПОВІДНОСТІ"])
    for row in rows:
        lines.append(f"\nПозиція {row['position']}. Топ-5 шифрованих літер: {row['top5']}.")
        for candidate in row["candidates"]:
            lines.append(f"  {row['cipher_mode']} -> {candidate['plain_mode']}: "
                         f"k={candidate['key']}, chi2={candidate['chi2']:.3f}")
    lines.extend([
        "", "ПЕРЕВІРКА",
        f"Довжина відкритого тексту: {len(plaintext)}; шифртексту: {len(ciphertext)}.",
        f"Найменший період відновленого ключа: {minimum_period(key)}.",
        f"Індекс шифртексту: {coincidence_index(ciphertext):.9f}.",
        f"Індекс відкритого тексту: {coincidence_index(plaintext):.9f}.",
        f"Повторне шифрування відтворює весь шифртекст: {roundtrip}.",
        "Повторне шифрування перевіряє узгодженість програми; воно саме по собі не доводить правильність ключа.",
        "Потрібно також прочитати весь результат, оцінити зв'язність і відсутність регулярних спотворень.",
        "", "ВІДКРИТИЙ ТЕКСТ (ПРОБІЛИ ТА ПУНКТУАЦІЮ НЕ ВІДНОВЛЮВАЛИ)", plaintext
    ])
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "key.txt").write_text(key, encoding="utf-8")
    (output_dir / "plaintext.txt").write_text(plaintext, encoding="utf-8")
    (output_dir / "initial_plaintext.txt").write_text(initial_plaintext, encoding="utf-8")
    (output_dir / "reencrypted.txt").write_text(transform(plaintext, key), encoding="utf-8")
    report = "\n".join(lines)
    (output_dir / "analysis_task3.txt").write_text(report, encoding="utf-8")
    with (output_dir / "key_statistics.csv").open("w", encoding="utf-8-sig", newline="") as f:
        fields = ["position", "n", "cipher_mode", "mode_count", "mode_frequency", "initial_key", "plain_mode", "key", "shift", "chi2", "top5"]
        writer = csv.DictWriter(f, fields, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    with (output_dir / "key_candidates.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Позиція", "Ранг", "y*", "x*", "Кандидат ключа", "Зсув", "chi2"])
        for row in rows:
            for rank, candidate in enumerate(row["candidates"], 1):
                writer.writerow([row['position'], rank, row['cipher_mode'], candidate['plain_mode'],
                                 candidate['key'], candidate['shift'], candidate['chi2']])
    with (output_dir / "reference_frequencies.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Літера", "Ймовірність із КП1 без пробілів"])
        writer.writerows(probabilities.items())
    print(report.split("\nЧАСТОТИ ТА АЛЬТЕРНАТИВНІ ВІДПОВІДНОСТІ")[0])
    print(f"\nНайменший період ключа: {minimum_period(key)}")
    print(f"Індекс відкритого тексту: {coincidence_index(plaintext):.9f}")
    print(f"Точне повторне шифрування: {roundtrip}")
    print(f"\nПочаток відкритого тексту:\n{plaintext[:300]}")
    print(f"\nРезультати збережено: {output_dir.resolve()}")


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="КП2: частотне відновлення ключа Віженера.")
    parser.add_argument("input", nargs="?", type=Path, default=base / "variant9.txt")
    parser.add_argument("--reference", type=Path, default=base / "frequencies_lab1.json",
                        help="JSON частот усіх 32 літер без пробілів із КП1.")
    parser.add_argument("--period", type=int, default=17)
    parser.add_argument("--output", type=Path, default=base / "results_task3")
    args = parser.parse_args()
    main(args.input, args.reference, args.period, args.output)
