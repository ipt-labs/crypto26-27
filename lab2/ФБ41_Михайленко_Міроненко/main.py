import os
from collections import Counter
from math import gcd

from tabulate import tabulate

from src.vigenere import (
    M, CHAR_TO_IDX, IDX_TO_CHAR, clean_text, encrypt, decrypt
)
from src.stats import calc_ic, calc_dr, get_blocks, avg_ic_for_r
from src.attack import RUS_FREQS, recover_key_chisquare, recover_key

MAX_R = 30
I_LANG = sum(p * p for p in RUS_FREQS.values())
I_RANDOM = 1 / M
THRESHOLD = (I_LANG + I_RANDOM) / 2


def read_clean(path):
    with open(path, "r", encoding="utf-8") as file:
        return clean_text(file.read())


def main():
    os.makedirs("data", exist_ok=True)
    cipher_path = "data/ciphertext_v10.txt"
    if not os.path.exists(cipher_path):
        raise SystemExit(f"Не знайдено файл {cipher_path}")

    ciphertext = read_clean(cipher_path)
    n = len(ciphertext)
    if n < 100:
        raise SystemExit("Шифртекст порожній або надто короткий.")

    print(f"=== Шифртекст варіанта 10: {n} символів ===")
    print(f"Алфавіт: {M} літери")
    print(f"I(ШТ) = {calc_ic(ciphertext):.6f}")
    print(f"I мови за КП №1 = {I_LANG:.6f}")
    print(f"I випадкового тексту = {I_RANDOM:.6f}")

    # 1. Перевірка власного тексту та впливу довжини ключа.
    sample_path = "data/sample_text.txt"
    if os.path.exists(sample_path):
        sample = read_clean(sample_path)
        print("\n--- Завдання 1. Шифрування власного відкритого тексту ---")
        print(f"Довжина очищеного тексту: {len(sample)} літер")
        if not 2000 <= len(sample) <= 3000:
            print("УВАГА: очищений текст має бути приблизно 2000–3000 літер.")
        keys = ["да", "мир", "ключ", "слово", "шелестстраниц"]
        rows = [["Відкритий текст", "-", "-", f"{calc_ic(sample):.6f}"]]
        for key in keys:
            clean_key = clean_text(key)
            encrypted = encrypt(sample, key)
            rows.append(["Шифртекст", clean_key, len(clean_key),
                         f"{calc_ic(encrypted):.6f}"])
            if decrypt(encrypted, key) != sample:
                raise RuntimeError("Помилка контрольної перевірки шифрування.")
        print(tabulate(rows, headers=["Текст", "Ключ", "r", "IC"],
                       tablefmt="github"))
    else:
        print("\nУВАГА: data/sample_text.txt не знайдено.")

    # 2. Пошук періоду.
    print(f"\n--- Завдання 2. Пошук періоду (r = 2..{MAX_R}) ---")
    stats = [
        (r, avg_ic_for_r(ciphertext, r), calc_dr(ciphertext, r))
        for r in range(2, min(MAX_R, n - 1) + 1)
    ]
    rows = [
        [r, f"{ic:.6f}", dr, f"{dr / (n-r):.6f}", n // r]
        for r, ic, dr in stats
    ]
    print(tabulate(rows, headers=["r", "Середній IC", "D_r",
                                  "D_r/(N-r)", "N/r"], tablefmt="github"))

    candidates = [r for r, ic, dr in stats if ic > THRESHOLD]
    print(f"\nПорогове значення IC = {THRESHOLD:.6f}")
    print(f"Кандидати, для яких середній IC вищий за поріг: {candidates}")

    if not candidates:
        raise SystemExit("Не знайдено кандидатів. Перевірте алфавіт і шифртекст.")

    # Найменший кандидат — попередня оцінка періоду. Додатково виводимо
    # кратні значення та не приховуємо неоднозначність статистичного методу.
    best_r = min(candidates)
    multiples = [r for r in candidates if r % best_r == 0]
    print(f"Попередньо обраний найменший кандидат: r = {best_r}")
    print(f"Кандидати, кратні {best_r}: {multiples}")
    print("Остаточний період потрібно підтвердити за якістю розшифрування.")

    print("\nАльтернативні кандидати зі спільними дільниками:")
    ic_by_r = {r: ic for r, ic, dr in stats}
    alt_rows = []
    for r in range(2, min(MAX_R, n - 1) + 1):
        common = gcd(r, best_r)
        if common > 1 and r != best_r:
            mixed = best_r // common
            expected_ic = I_LANG / mixed + (1 - 1 / mixed) * I_RANDOM
            alt_rows.append([r, common, mixed,
                             f"{ic_by_r[r]:.6f}", f"{expected_ic:.6f}"])
    print(tabulate(alt_rows,
                   headers=["r", "gcd(r, r*)", "К-сть зсувів",
                            "IC факт.", "IC оцінка"],
                   tablefmt="github") if alt_rows else "Немає.")

    # 3. Відновлення ключа двома способами.
    print(f"\n--- Завдання 3. Відновлення ключа (r = {best_r}) ---")
    blocks = get_blocks(ciphertext, best_r)
    chi_key = recover_key_chisquare(ciphertext, best_r)
    naive_key = recover_key(ciphertext, best_r, "о")

    rows = []
    for i, block in enumerate(blocks):
        y, count = Counter(block).most_common(1)[0]
        candidates_for_x = []
        for plain_char in "оеа":
            candidates_for_x.append(
                IDX_TO_CHAR[(CHAR_TO_IDX[y] - CHAR_TO_IDX[plain_char]) % M]
            )
        rows.append([i, y, count, len(block), *candidates_for_x, chi_key[i]])
    print(tabulate(rows, headers=["i", "Найчастіша літера", "К-сть",
                                  "Довжина блоку", "k для о", "k для е",
                                  "k для а", "Ключ χ²"], tablefmt="github"))
    print(f"Наївний ключ (x*=о): {naive_key}")
    print(f"Ключ за χ²:          {chi_key}")

    plaintext = decrypt(ciphertext, chi_key)
    os.makedirs("data", exist_ok=True)
    with open("data/decrypted_v10.txt", "w", encoding="utf-8") as file:
        file.write(plaintext)

    print(f"\nI розшифрованого тексту = {calc_ic(plaintext):.6f}")
    print("Початок розшифрування:")
    print(plaintext[:500])
    print("\nКінець розшифрування:")
    print(plaintext[-300:])

    # 4. Експеримент зі зміною одного символу ключа.
    print("\n--- Завдання 4. Зміна одного символу ключа ---")
    position = 0
    replacement = "а" if chi_key[position] != "а" else "б"
    wrong_key = (chi_key[:position] + replacement + chi_key[position + 1:])
    expected_shift = (CHAR_TO_IDX[chi_key[position]] -
                      CHAR_TO_IDX[replacement]) % M
    wrong_plaintext = decrypt(ciphertext, wrong_key)
    differences = [i for i in range(n)
                   if plaintext[i] != wrong_plaintext[i]]
    changed_columns = sorted({i % best_r for i in differences})
    actual_shifts = sorted({
        (CHAR_TO_IDX[wrong_plaintext[i]] -
         CHAR_TO_IDX[plaintext[i]]) % M for i in differences
    })

    print(f"Початковий ключ: {chi_key}")
    print(f"Змінений ключ:   {wrong_key}")
    print(f"Змінено позицію ключа: {position}")
    print(f"Очікуваний зсув: {expected_shift} за модулем {M}")
    print(f"Змінено символів тексту: {len(differences)} із {n}")
    print(f"Позиції за модулем r: {changed_columns}")
    print(f"Фактичні зсуви: {actual_shifts}")
    if changed_columns != [position] or actual_shifts != [expected_shift]:
        print("УВАГА: результат експерименту не збігся з прогнозом.")
    else:
        print("Експеримент підтвердив прогноз: змінюється кожна r-та літера "
              "відповідного блоку.")


if __name__ == "__main__":
    main()
