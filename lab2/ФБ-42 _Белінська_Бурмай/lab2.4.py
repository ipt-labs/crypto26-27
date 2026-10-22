from pathlib import Path
import argparse
import csv

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
INDEX = {c: i for i, c in enumerate(ALPHABET)}
M = len(ALPHABET)


def read_letters(path):
    raw = path.read_text(encoding="utf-8-sig").lower()
    invalid = set(raw) - set(ALPHABET) - set(" \t\r\n\ufeff")
    if invalid:
        raise ValueError(f"Файл {path.name}: сторонні символи {sorted(invalid)}")
    text = "".join(c for c in raw if c in INDEX)
    if not text:
        raise ValueError(f"Файл {path.name} порожній.")
    return text


def decrypt(ciphertext, key):
    return "".join(ALPHABET[(INDEX[c] - INDEX[key[i % len(key)]]) % M]
                   for i, c in enumerate(ciphertext))


def main(cipher_path, key_path, position, replacement, output_dir):
    ciphertext = read_letters(cipher_path)
    key = read_letters(key_path)
    n, r = len(ciphertext), len(key)
    j = position - 1
    if not 0 <= j < r:
        raise ValueError(f"Позиція ключа має бути від 1 до {r}.")
    if len(replacement) != 1 or replacement not in INDEX:
        raise ValueError("Заміна має бути однією літерою заданого алфавіту.")
    if replacement == key[j]:
        raise ValueError("Новий символ має відрізнятися від початкового.")
    wrong_key = key[:j] + replacement + key[j + 1:]
    if sum(a != b for a, b in zip(key, wrong_key)) != 1:
        raise AssertionError("Потрібно змінити рівно один символ ключа.")

    # Прогноз створюється й записується ДО розшифрування неправильним ключем.
    predicted_positions = list(range(j, n, r))
    predicted_count = (n - 1 - j) // r + 1 if j < n else 0
    shift = (INDEX[key[j]] - INDEX[replacement]) % M
    signed_shift = shift if shift <= M // 2 else shift - M
    prediction = (
        "ПРОГНОЗ ДО ЕКСПЕРИМЕНТУ\n"
        f"Шифртекст: {cipher_path.name}, n={n}.\n"
        f"Правильний ключ: {key}; довжина r={r}.\n"
        f"Позиція ключа (від 1): {position}; заміна {key[j]} -> {replacement}.\n"
        f"Ключ із помилкою: {wrong_key}.\n"
        f"Позиції змін у тексті (від 1): {position}+t*{r}, t=0,1,..., доки позиція <= {n}.\n"
        f"Прогнозована кількість змін: {predicted_count}.\n"
        f"Прогнозована кількість незмінних літер: {n-predicted_count}.\n"
        f"Зсув пошкоджених літер: {signed_shift:+d} за модулем {M} (залишок {shift}).\n"
        "Інші позиції не зміняться. Накопичення помилки та її поширення на сусідні літери не буде.\n"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "prediction_before_experiment.txt").write_text(prediction, encoding="utf-8")
    print(prediction, flush=True)

    # Проведення експерименту після запису прогнозу.
    correct_text = decrypt(ciphertext, key)
    wrong_text = decrypt(ciphertext, wrong_key)
    actual_positions = [i for i, (a, b) in enumerate(zip(correct_text, wrong_text)) if a != b]
    positions_match = actual_positions == predicted_positions
    shifts_match = all((INDEX[wrong_text[i]] - INDEX[correct_text[i]]) % M == shift
                       for i in actual_positions)
    count_match = len(actual_positions) == predicted_count
    if not (positions_match and shifts_match and count_match):
        raise AssertionError("Експеримент не відповідає прогнозу: перевірте реалізацію.")

    (output_dir / "plaintext_correct.txt").write_text(correct_text, encoding="utf-8")
    (output_dir / "plaintext_wrong_key.txt").write_text(wrong_text, encoding="utf-8")
    (output_dir / "wrong_key.txt").write_text(wrong_key, encoding="utf-8")
    with (output_dir / "changed_positions.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream, delimiter=";")
        writer.writerow(["Позиція в тексті (від 1)", "Позиція ключа (від 1)",
                         "Правильна літера", "Помилкова літера", "Зсув mod 32"])
        for i in actual_positions:
            writer.writerow([i + 1, position, correct_text[i], wrong_text[i], shift])

    samples = ["| Позиція тексту | Правильна літера | Помилкова літера |",
               "|---:|:---:|:---:|"]
    samples += [f"| {i+1} | {correct_text[i]} | {wrong_text[i]} |" for i in actual_positions[:15]]
    if actual_positions:
        last = actual_positions[-1]
        samples.append(f"| {last+1} (остання) | {correct_text[last]} | {wrong_text[last]} |")
    percentage = 100 * len(actual_positions) / n
    report = r'''# КП2. Завдання 4. Дослідження впливу помилки у ключі

**Варіант 9**

## Мета та вхідні дані

Дослідити, як заміна одного символу правильного ключа Віженера впливає на результат розшифрування того самого шифртексту. Використано variant9.txt і ключ, відновлений у завданні 3. Повторно відновлювати ключ у цьому експерименті не потрібно.

| Параметр | Значення |
|---|---|
| Кількість літер шифртексту | __N__ |
| Правильний ключ | `__KEY__` |
| Довжина ключа | __R__ |
| Змінена позиція ключа (від 1) | __POSITION__ |
| Заміна | `__OLD__ → __NEW__` |
| Ключ із помилкою | `__WRONG_KEY__` |

Алфавіт: `абвгдежзийклмнопрстуфхцчшщъыьэюя`. Розмір алфавіту m=32; літери нумеруються від нуля. Довжина ключа не змінюється.

## Прогноз до експерименту

Ключ періодично повторюється з періодом r. Зміна одного символу вплине лише на ті позиції тексту, де використовується саме він. Для зміненої позиції ключа j за нумерації від нуля це індекси i=j,j+r,j+2r,… . У звіті позиції тексту й ключа для зручності нумеруються від 1.

Правильне та помилкове розшифрування пошкоджених позицій мають вигляд:

$$x_i=(y_i-k_j)\bmod32,$$

$$x'_i=(y_i-k'_j)\bmod32.$$

Звідси:

$$x'_i=(x_i+k_j-k'_j)\bmod32.$$

Отже, кожна пошкоджена літера матиме один і той самий додатковий циклічний зсув. Решта літер залишиться правильною.

Для обраної заміни __OLD__→__NEW__ індекси символів ключа дорівнюють __OLD_INDEX__ та __NEW_INDEX__. Прогнозований зсув відкритих літер становить __SIGNED_SHIFT__ за модулем 32, або __SHIFT__ у вигляді невід'ємного залишку.

Прогнозовані позиції помилок (нумерація від 1): __POSITION__+t·__R__, де t≥0 і позиція не перевищує __N__.

Точна кількість пошкоджених літер при j<n:

$$N_{помилок}=\left\lfloor\frac{n-1-j}{r}\right\rfloor+1.$$

Для заданих параметрів очікується __COUNT__ змінених літер і __UNCHANGED__ незмінних. Для довгого тексту частка пошкоджень близька до 1/r; точне значення залежить від довжини тексту та позиції зміненого символу ключа.

Прогноз записується програмою у prediction_before_experiment.txt до розшифрування неправильним ключем. Це прогноз на основі формули, а не висновок із уже отриманого помилкового тексту.

## Проведення експерименту

1. Той самий шифртекст розшифровано правильним ключем.
2. Змінено один символ ключа без зміни його довжини.
3. Той самий шифртекст розшифровано ключем із помилкою.
4. Два результати порівняно посимвольно.
5. Фактичні позиції, кількість змін і зсув кожної зміненої літери перевірено за прогнозом.

Початок правильного тексту:

```text
__CORRECT_START__
```

Початок тексту після помилки в ключі:

```text
__WRONG_START__
```

Пробіли та пунктуацію не додавали. Повні результати збережено у plaintext_correct.txt та plaintext_wrong_key.txt.

## Результати та порівняння з прогнозом

| Показник | Прогноз | Експеримент |
|---|---:|---:|
| Кількість змінених літер | __COUNT__ | __ACTUAL_COUNT__ |
| Кількість незмінних літер | __UNCHANGED__ | __ACTUAL_UNCHANGED__ |
| Крок між зміненими позиціями | __R__ | __R__ |
| Додатковий зсув змінених літер mod 32 | __SHIFT__ | __SHIFT__ |

Фактична частка пошкоджених літер: **__PERCENT__%**. Усі прогнозовані позиції збіглися з фактичними. На інших позиціях змін немає. Довжина обох результатів становить __N__ літер.

Приклади змін і остання пошкоджена позиція:

__SAMPLES__

Повний перелік усіх __COUNT__ змін наведено у changed_positions.csv. За нумерації від нуля кожен індекс зміненої літери дає залишок j при діленні на r. Для цієї заміни перша пошкоджена літера __FIRST_CORRECT__ переходить у __FIRST_WRONG__.

## Пояснення ефекту

У Віженера кожна літера розшифровується незалежно від попередніх: від її числового значення віднімається лише поточний символ циклічного ключа. Тому помилка в одному символі ключа повторюється через кожні r позицій і не накопичується. Вона не поширюється на всі наступні літери й не впливає на інші позиції ключа.

У цьому експерименті саме замінено символ. Якби символ вставили або видалили, змінилися б довжина та вирівнювання ключа, і це був би інший експеримент.

## Висновок

Після заміни одного символу ключа `__KEY__` на `__WRONG_KEY__` змінилися лише __COUNT__ із __N__ літер (__PERCENT__%). Помилки з'являються з періодом __R__ і мають однаковий циклічний зсув __SIGNED_SHIFT__. Усі інші літери залишилися правильними. Прогноз, сформований до експерименту, повністю підтвердився. Результат демонструє відсутність лавинного поширення помилки в шифрі Віженера з періодичним ключем.
'''
    values = {
        "N": n, "KEY": key, "R": r, "POSITION": position,
        "OLD": key[j], "NEW": replacement, "WRONG_KEY": wrong_key,
        "OLD_INDEX": INDEX[key[j]], "NEW_INDEX": INDEX[replacement],
        "SIGNED_SHIFT": f"{signed_shift:+d}", "SHIFT": shift,
        "COUNT": predicted_count, "UNCHANGED": n - predicted_count,
        "ACTUAL_COUNT": len(actual_positions), "ACTUAL_UNCHANGED": n - len(actual_positions),
        "PERCENT": f"{percentage:.6f}".replace(".", ","),
        "CORRECT_START": correct_text[:170], "WRONG_START": wrong_text[:170],
        "SAMPLES": "\n".join(samples),
        "FIRST_CORRECT": correct_text[actual_positions[0]] if actual_positions else "—",
        "FIRST_WRONG": wrong_text[actual_positions[0]] if actual_positions else "—"
    }
    for name, value in values.items():
        report = report.replace(f"__{name}__", str(value))
    (output_dir / "report_task4_uk.md").write_text(report, encoding="utf-8")
    print("РЕЗУЛЬТАТ ЕКСПЕРИМЕНТУ")
    print(f"Змінено літер: {len(actual_positions)} із {n} ({percentage:.6f}%)")
    print(f"Незмінних літер: {n - len(actual_positions)}")
    print("Перші позиції помилок:", [i + 1 for i in actual_positions[:15]])
    print("Остання позиція помилки:", actual_positions[-1] + 1 if actual_positions else "немає")
    print(f"Позиції, кількість та зсув збіглися з прогнозом: {positions_match and shifts_match and count_match}")
    print(f"Результати збережено: {output_dir.resolve()}")


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="КП2, завдання 4: помилка в одному символі ключа.")
    parser.add_argument("input", nargs="?", type=Path, default=base / "variant9.txt")
    parser.add_argument("--key-file", type=Path, default=base / "key.txt")
    parser.add_argument("--position", type=int, default=1, help="Позиція символу ключа від 1.")
    parser.add_argument("--replacement", default="г", help="Новий символ ключа.")
    parser.add_argument("--output", type=Path, default=base / "results_task4")
    args = parser.parse_args()
    main(args.input, args.key_file, args.position, args.replacement, args.output)
