from pathlib import Path
from collections import Counter
from statistics import mean, pstdev
import argparse
import csv

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"


def prepare_ciphertext(raw):
    text = raw.lower()
    invalid = set(text) - set(ALPHABET) - set(" \t\r\n\ufeff")
    if invalid:
        raise ValueError(f"Сторонні символи у шифртексті: {sorted(invalid)}")
    return "".join(c for c in text if c in ALPHABET)


def coincidence_index(text):
    n = len(text)
    if n < 2:
        raise ValueError("Для індексу потрібно щонайменше дві літери.")
    return sum(v * (v - 1) for v in Counter(text).values()) / (n * (n - 1))


def analyze_period(text, r):
    blocks = [text[j::r] for j in range(r)]
    indices = [coincidence_index(block) for block in blocks]
    matches = sum(text[i] == text[i + r] for i in range(len(text) - r))
    return {
        "r": r,
        "mean_ic": mean(indices),
        "min_ic": min(indices),
        "max_ic": max(indices),
        "std_ic": pstdev(indices),
        "min_length": min(map(len, blocks)),
        "max_length": max(map(len, blocks)),
        "matches": matches,
        "match_rate": matches / (len(text) - r),
        "block_indices": indices
    }


def format_table(rows):
    lines = [
        f"{'r':>3} {'Середній I':>12} {'Мін. I':>12} {'Макс. I':>12} {'D_r':>6} {'D_r/(n-r)':>12}",
        "-" * 64
    ]
    for row in rows:
        lines.append(
            f"{row['r']:>3} {row['mean_ic']:>12.9f} "
            f"{row['min_ic']:>12.9f} {row['max_ic']:>12.9f} "
            f"{row['matches']:>6} {row['match_rate']:>12.9f}"
        )
    return "\n".join(lines)


def main(input_file, output_dir, max_period):
    if max_period < 30:
        raise ValueError("За умовою потрібно перевірити періоди щонайменше до 30.")
    raw = input_file.read_text(encoding="utf-8-sig")
    text = prepare_ciphertext(raw)
    if len(text) < 2 * max_period:
        raise ValueError("Недостатньо тексту: потрібні принаймні дві літери в кожній послідовності.")

    rows = [analyze_period(text, r) for r in range(1, max_period + 1)]
    ranked = sorted(rows, key=lambda row: row["mean_ic"], reverse=True)
    primary = ranked[0]
    r = primary["r"]
    other = [row for row in rows if row["r"] != r]
    strongest_shift = max(other, key=lambda row: row["match_rate"])

    reasons = {r: "Основний кандидат: найбільший середній індекс у перевіреному діапазоні."}

    def add(candidate, reason):
        if candidate in reasons:
            reasons[candidate] += " " + reason
        else:
            reasons[candidate] = reason

    for row in ranked[1:3]:
        add(row["r"], "Один із найвищих альтернативних середніх індексів.")
    add(strongest_shift["r"], "Найбільша альтернативна частка збігів при зсуві.")
    add(1, "Перевірка випадку одного постійного зсуву (шифр Цезаря).")
    for factor in (2, 3):
        candidate = factor * r
        if candidate > max_period and len(text) >= 2 * candidate:
            add(candidate, f"Додаткова перевірка кратного періоду: {factor} × {r}.")

    by_period = {row["r"]: row for row in rows}
    alternatives = [by_period[c] if c in by_period else analyze_period(text, c)
                    for c in reasons]

    lines = [
        "КП2. ЗАВДАННЯ 2. ВИЗНАЧЕННЯ ПЕРІОДУ ШИФРУ ВІЖЕНЕРА",
        f"Вхідний файл: {input_file.name}",
        f"Кількість літер: {len(text)}; алфавіт: {len(ALPHABET)} літери.",
        f"Індекс усього шифртексту: {coincidence_index(text):.9f}",
        f"Орієнтир рівномірної моделі: 1/32 = {1 / 32:.9f}",
        "Мовні частоти з КП1 не надані; конкретне теоретичне мовне значення не підставляється.",
        "",
        "МЕТОДИ",
        "1. Для кожного r формуються послідовності text[j::r].",
        "   Обчислюються їх індекси та незважене середнє цих індексів.",
        "2. D_r — кількість рівностей text[i] == text[i+r].",
        "   D_r/(n-r) — частка збігів із поправкою на кількість порівнянь.",
        "",
        f"ПОВНА ТАБЛИЦЯ ДЛЯ r=1..{max_period}",
        format_table(rows),
        "",
        "ОСНОВНИЙ КАНДИДАТ",
        f"r={r}: середній I={primary['mean_ic']:.9f}; "
        f"D_r={primary['matches']}; частка збігів={primary['match_rate']:.9f}.",
        f"Послідовності мають по {primary['min_length']}–{primary['max_length']} літер.",
        "За правильного періоду кожна послідовність зашифрована постійним зсувом.",
        "Цей зсув зберігає індекс, оскільки лише переставляє частоти літер.",
        "",
        "АЛЬТЕРНАТИВНІ КАНДИДАТИ ТА КРАТНІ ПЕРІОДИ",
        format_table(alternatives)
    ]

    output_dir.mkdir(parents=True, exist_ok=True)
    report = "\n".join(lines)
    (output_dir / "analysis_task2.txt").write_text(report, encoding="utf-8")
    fields = ["r", "mean_ic", "min_ic", "max_ic", "std_ic", "min_length", "max_length", "matches", "match_rate"]
    with (output_dir / "periods.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows + [row for row in alternatives if row["r"] > max_period])
    with (output_dir / "block_indices.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["r", "Номер послідовності (від 0)", "Кількість літер", "Індекс"])
        for row in rows + [a for a in alternatives if a["r"] > max_period]:
            for j, index in enumerate(row["block_indices"]):
                writer.writerow([row["r"], j, len(text[j::row["r"]]), index])
    print(report)
    print(f"\nРезультати збережено: {output_dir.resolve()}")


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="КП2, завдання 2: статистичний пошук періоду.")
    parser.add_argument("input", nargs="?", type=Path, default=base / "variant9.txt")
    parser.add_argument("--output", type=Path, default=base / "results_task2")
    parser.add_argument("--max-period", type=int, default=30)
    args = parser.parse_args()
    main(args.input, args.output, args.max_period)

