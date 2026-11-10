import math
import re
from collections import Counter


# ==================== ПОЧАТОК ЕТАПУ 1 ====================
print("=" * 60)
print("ПОЧАТОК ЕТАПУ 1: МАТЕМАТИЧНІ ОПЕРАЦІЇ МОДУЛЯРНОЇ АРИФМЕТИКИ")
print("=" * 60)

def extended_gcd(a: int, b: int):
    r0, r1 = a, b
    u0, u1 = 1, 0
    v0, v1 = 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return r0, u0, v0

def mod_inverse(a: int, n: int):
    a %= n
    d, u, _ = extended_gcd(a, n)
    if d != 1:
        return None
    return u % n

def solve_linear_congruence(a: int, b: int, n: int):
    a %= n
    b %= n
    d, _, _ = extended_gcd(a, n)
    if d == 1:
        inv = mod_inverse(a, n)
        return [(b * inv) % n]
    if b % d != 0:
        return []
    a1 = a // d
    b1 = b // d
    n1 = n // d
    inv = mod_inverse(a1, n1)
    x0 = (b1 * inv) % n1
    return [(x0 + k * n1) % n for k in range(d)]

test_inv = mod_inverse(200, 961)
test_single = solve_linear_congruence(128, 614, 961)
test_multi = solve_linear_congruence(155, 248, 961)
print(f"Перевірка оберненого елемента: 200^(-1) mod 961 = {test_inv}")
print(f"Порівняння з 1 розв'язком (128*a = 614 mod 961): {test_single}")
print(f"Порівняння з декількома розв'язками (155*a = 248 mod 961), кількість = {len(test_multi)}:")
print(f"  {test_multi}")

print("-" * 60)
print("КІНЕЦЬ ЕТАПУ 1")
print("=" * 60 + "\n")
# ==================== КІНЕЦЬ ЕТАПУ 1 ====================


# ==================== ПОЧАТОК ЕТАПУ 2 ====================
print("=" * 60)
print("ПОЧАТОК ЕТАПУ 2: ЧАСТОТНИЙ АНАЛІЗ БІГРАМ ШИФРТЕКСТУ (ЗА КОДОМ КП №1)")
print("=" * 60)

RUSSIAN_LETTERS = "абвгдежзийклмнопрстуфхцчшщьыэюя"
ALPHABET_WITH_SPACE = set(RUSSIAN_LETTERS + " ")
M = len(RUSSIAN_LETTERS)
M2 = M * M
CHAR_TO_IDX = {ch: idx for idx, ch in enumerate(RUSSIAN_LETTERS)}
IDX_TO_CHAR = {idx: ch for idx, ch in enumerate(RUSSIAN_LETTERS)}

def preprocess(raw_text: str, keep_spaces: bool = False) -> str:
    text = raw_text.lower()
    text = text.replace("ё", "е").replace("ъ", "ь")
    text = "".join(ch if ch in ALPHABET_WITH_SPACE else " " for ch in text)
    text = re.sub(r" +", " ", text).strip()
    if not keep_spaces:
        text = text.replace(" ", "")
    return text

def calc_entropy(counts: Counter, total: int) -> float:
    h = 0.0
    for c in counts.values():
        p = c / total
        h -= p * math.log2(p)
    return h

def bigram_to_num(bg: str) -> int:
    return CHAR_TO_IDX[bg[0]] * M + CHAR_TO_IDX[bg[1]]

def num_to_bigram(num: int) -> str:
    return IDX_TO_CHAR[num // M] + IDX_TO_CHAR[num % M]

def analyze_text(text: str, label: str = "ШИФРТЕКСТ БЕЗ ПРОБІЛІВ"):
    total = len(text)
    counts = Counter(text)
    h1 = calc_entropy(counts, total)

    bg_over = [text[i:i+2] for i in range(total - 1)]
    h2_over = calc_entropy(Counter(bg_over), len(bg_over)) / 2.0

    bg_nonover = [text[i:i+2] for i in range(0, total - 1, 2)]
    h2_nonover = calc_entropy(Counter(bg_nonover), len(bg_nonover)) / 2.0

    print(f"{label} (алфавіт із {M} символів, довжина: {total})")
    print("Топ-5 символів (символ, кількість, частка):")
    for ch, n in counts.most_common(5):
        display_ch = f"'{ch}'"
        print(f"{display_ch:>15} {n:>10} {n/total:>8.4f}")

    print("Топ-5 біграм, що ПЕРЕТИНАЮТЬСЯ:")
    for bg, n in Counter(bg_over).most_common(5):
        display_bg = f"'{bg}' (Y={bigram_to_num(bg):>3})"
        print(f"{display_bg:>15} {n:>10} {n/len(bg_over):>8.4f}")

    print("Топ-5 біграм, що НЕ перетинаються:")
    top5_nonover = Counter(bg_nonover).most_common(5)
    for bg, n in top5_nonover:
        display_bg = f"'{bg}' (Y={bigram_to_num(bg):>3})"
        print(f"{display_bg:>15} {n:>10} {n/len(bg_nonover):>8.4f}")

    print(f"{'H1':<15} = {h1:.4f} біт/симв.")
    print(f"{'H2 (перетин.)':<15} = {h2_over:.4f} біт/симв.")
    print(f"{'H2 (без перет.)':<15} = {h2_nonover:.4f} біт/симв.")
    return [bg for bg, _ in top5_nonover]

file_name = "07.txt"
with open(file_name, encoding="cp1251", errors="ignore") as f:
    raw_data = f.read()

cipher_text = preprocess(raw_data, keep_spaces=False)
cipher_top5_bigrams = analyze_text(cipher_text, "ШИФРТЕКСТ ВАРІАНТА 07")

print("-" * 60)
print("КІНЕЦЬ ЕТАПУ 2")
print("=" * 60 + "\n")
# ==================== КІНЕЦЬ ЕТАПУ 2 ====================


# ==================== ПОЧАТОК ЕТАПУ 3 ====================
print("=" * 60)
print("ПОЧАТОК ЕТАПУ 3: ПЕРЕБІР СПІВСТАВЛЕНЬ БІГРАМ ТА ПОШУК КАНДИДАТІВ НА КЛЮЧ (a, b)")
print("=" * 60)

LANG_TOP5_BIGRAMS = ["ст", "но", "то", "на", "ен"]

def generate_key_candidates(lang_bigrams, cipher_bigrams):
    x_nums = [bigram_to_num(bg) for bg in lang_bigrams]
    y_nums = [bigram_to_num(bg) for bg in cipher_bigrams]
    candidates = set()
    total_checked = 0
    multi_solution_cases = 0
    no_solution_cases = 0

    for i in range(len(x_nums)):
        for j in range(len(x_nums)):
            if i == j:
                continue
            for k in range(len(y_nums)):
                for l in range(len(y_nums)):
                    if k == l:
                        continue
                    total_checked += 1
                    dx = (x_nums[i] - x_nums[j]) % M2
                    dy = (y_nums[k] - y_nums[l]) % M2
                    a_solutions = solve_linear_congruence(dx, dy, M2)
                    if len(a_solutions) == 0:
                        no_solution_cases += 1
                    elif len(a_solutions) > 1:
                        multi_solution_cases += 1
                    for a in a_solutions:
                        d_a, _, _ = extended_gcd(a, M)
                        if a > 0 and d_a == 1:
                            b = (y_nums[k] - a * x_nums[i]) % M2
                            candidates.add((a, b))

    print(f"Топ-5 біграм російської мови: {[f'{bg} (X={bigram_to_num(bg)})' for bg in lang_bigrams]}")
    print(f"Топ-5 біграм шифртексту:      {[f'{bg} (Y={bigram_to_num(bg)})' for bg in cipher_bigrams]}")
    print(f"Усього розглянуто пар співставлень: {total_checked}")
    print(f"Випадків без розв'язків лінійного порівняння: {no_solution_cases}")
    print(f"Випадків із декількома розв'язками (по 31 розв'язку): {multi_solution_cases}")
    print(f"Знайдено унікальних допустимих кандидатів на ключ (a, b): {len(candidates)}")
    return sorted(candidates)

key_candidates = generate_key_candidates(LANG_TOP5_BIGRAMS, cipher_top5_bigrams)
print("Перші 10 кандидатів на ключ (a, b):", key_candidates[:10])

print("-" * 60)
print("КІНЕЦЬ ЕТАПУ 3")
print("=" * 60 + "\n")
# ==================== КІНЕЦЬ ЕТАПУ 3 ====================


# ==================== ПОЧАТОК ЕТАПУ 4 ====================
print("=" * 60)
print("ПОЧАТОК ЕТАПУ 4: ДЕШИФРУВАННЯ КАНДИДАТІВ ТА АВТОМАТИЧНЕ РОЗПІЗНАВАННЯ МОВИ")
print("=" * 60)

FORBIDDEN_BIGRAMS = {
    "аь", "оь", "еь", "иь", "уь", "ыь", "эь", "юь", "яь",
    "аы", "оы", "еы", "иы", "уы", "ыы", "эы", "юы", "яы",
    "жы", "шы", "чя", "щя", "чю", "щю", "йь", "йы", "ьь", "ьы"
}

def decrypt_affine_bigram(cipher_str: str, a: int, b: int) -> str:
    inv_a = mod_inverse(a, M2)
    if inv_a is None:
        return ""
    bg_nonover = [cipher_str[i:i+2] for i in range(0, len(cipher_str) - 1, 2)]
    decrypted = []
    for bg in bg_nonover:
        y = bigram_to_num(bg)
        x = (inv_a * (y - b)) % M2
        decrypted.append(num_to_bigram(x))
    return "".join(decrypted)

def is_meaningful_russian_text(text: str):
    n = len(text)
    if n == 0:
        return False, {}
    freq_oae = sum(text.count(ch) for ch in "оае") / n
    freq_rare = sum(text.count(ch) for ch in "фщэ") / n
    forbidden_count = sum(1 for i in range(n - 1) if text[i:i+2] in FORBIDDEN_BIGRAMS)
    cross_bigrams = [text[i:i+2] for i in range(1, n - 1, 2)]
    top_cross_set = {"ст", "но", "то", "на", "ен", "ов", "ни", "ра", "во", "ко"}
    cross_score = sum(1 for bg in cross_bigrams if bg in top_cross_set) / len(cross_bigrams)
    h1 = calc_entropy(Counter(text), n)

    passed = (
        forbidden_count == 0
        and freq_oae >= 0.22
        and freq_rare <= 0.02
        and cross_score >= 0.05
        and h1 <= 4.55
    )
    metrics = {
        "freq_oae": freq_oae,
        "freq_rare": freq_rare,
        "forbidden_count": forbidden_count,
        "cross_score": cross_score,
        "h1": h1,
    }
    return passed, metrics

found_keys = []
rejected_count = 0

for a, b in key_candidates:
    candidate_text = decrypt_affine_bigram(cipher_text, a, b)
    passed, metrics = is_meaningful_russian_text(candidate_text)
    if passed:
        found_keys.append((a, b, candidate_text, metrics))
        print(f"Кандидат (a={a}, b={b}) ПРОЙШОВ перевірку:")
        print(f"  Сума частот ('о','а','е'): {metrics['freq_oae']:.4f} (поріг >= 0.22)")
        print(f"  Сума частот ('ф','щ','э'): {metrics['freq_rare']:.4f} (поріг <= 0.02)")
        print(f"  Заборонених біграм:        {metrics['forbidden_count']} (поріг == 0)")
        print(f"  Часті біграми на перетині: {metrics['cross_score']:.4f} (поріг >= 0.05)")
        print(f"  Ентропія H1:               {metrics['h1']:.4f} біт/симв. (поріг <= 4.55)")
    else:
        rejected_count += 1

print(f"Відкинуто неправильних кандидатів: {rejected_count} із {len(key_candidates)}")
print(f"Знайдено змістовних текстів: {len(found_keys)}")

print("-" * 60)
print("КІНЕЦЬ ЕТАПУ 4")
print("=" * 60 + "\n")
# ==================== КІНЕЦЬ ЕТАПУ 4 ====================


# ==================== ПОЧАТОК ЕТАПУ 5 ====================
print("=" * 60)
print("ПОЧАТОК ЕТАПУ 5: РЕЗУЛЬТАТИ ДЕШИФРУВАННЯ ТА ПЕРЕВІРКА ВІДКРИТОГО ТЕКСТУ")
print("=" * 60)

if found_keys:
    best_a, best_b, decrypted_text, best_metrics = found_keys[0]
    inv_best_a = mod_inverse(best_a, M2)
    print(f"Знайдений ключ шифрування: a = {best_a}, b = {best_b}")
    print(f"Обернений елемент для розшифрування: a^(-1) mod {M2} = {inv_best_a}\n")

    analyze_text(decrypted_text, "РОЗШИФРОВАНИЙ ВІДКРИТИЙ ТЕКСТ")

    print("\nПерші 400 символів розшифрованого тексту:")
    print(decrypted_text[:400])
    print("\nОстанні 250 символів розшифрованого тексту:")
    print(decrypted_text[-250:])

    output_file = "decrypted_07.txt"
    with open(output_file, "w", encoding="utf-8") as out_f:
        out_f.write(decrypted_text)
    print(f"\nПовний розшифрований текст збережено у файл: {output_file}")

print("-" * 60)
print("КІНЕЦЬ ЕТАПУ 5")
print("=" * 60)
# ==================== КІНЕЦЬ ЕТАПУ 5 ====================