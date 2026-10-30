import os
from collections import Counter

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
m = len(alphabet)  # 31
n = m * m          # 961 = m^2, модуль для біграм

# п'ять найчастіших біграм російської мови
lang_top = ["ст", "но", "то", "на", "ен"]


# розширений алгоритм Евкліда: повертає d, u, v, де d = gcd(a, b) = u*a + v*b
def egcd(a, b):
    r0, r1 = a, b
    u0, u1 = 1, 0
    v0, v1 = 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return r0, u0, v0


# обернений елемент a^(-1) за модулем mod (None, якщо gcd(a, mod) != 1)
def inverse(a, mod):
    d, u, v = egcd(a % mod, mod)
    if d != 1:
        return None
    return u % mod


# розв'язування ax ≡ b (mod mod), повертає список усіх розв'язків
def solve_linear(a, b, mod):
    a = a % mod
    b = b % mod
    d = egcd(a, mod)[0]  # d = gcd(a, mod)

    if b % d != 0:  # якщо b не ділиться на d, розв'язків нема
        return []

    a1 = a // d
    b1 = b // d
    n1 = mod // d
    x0 = (b1 * inverse(a1, n1)) % n1  # єдиний розв'язок a1*x = b1 (mod n1)

    solutions = []
    for k in range(d):
        solutions.append(x0 + k * n1)
    return solutions


# k найчастіших неперетинних біграм
def top_bigrams(text, k=5):
    bigrams = []
    for i in range(0, len(text) - 1, 2):
        bigrams.append(text[i : i + 2])
    counts = Counter(bigrams)
    return counts.most_common(k), len(bigrams)


# переведення біграми у число X = x1*m + x2
def bigram_to_number(bigram):
    x1 = alphabet.index(bigram[0])
    x2 = alphabet.index(bigram[1])
    return x1 * m + x2


# переведення числа в біграму
def number_to_bigram(X):
    x1 = X // m
    x2 = X % m
    return alphabet[x1] + alphabet[x2]


# шифрування: Y = (a*X + b) mod m^2
def affine_encrypt(text, a, b):
    result = ""
    for i in range(0, len(text) - 1, 2):
        X = bigram_to_number(text[i : i + 2])
        Y = (a * X + b) % n
        result += number_to_bigram(Y)
    return result


# розшифрування: X = a^(-1) * (Y - b) mod m^2
def affine_decrypt(text, a, b):
    a_inv = inverse(a, n)
    result = ""
    for i in range(0, len(text) - 1, 2):
        Y = bigram_to_number(text[i : i + 2])
        X = (a_inv * (Y - b)) % n
        result += number_to_bigram(X)
    return result


# кандидати на ключ (a, b) за двома відповідностями X1 -> Y1, X2 -> Y2
def find_keys(X1, Y1, X2, Y2):
    keys = []
    for a in solve_linear(X1 - X2, Y1 - Y2, n):
        if egcd(a, m)[0] != 1:  # a має бути взаємно простим з m
            continue
        b = (Y1 - a * X1) % n    # b = (Y1 - a*X1) mod m^2
        keys.append((a, b))
    return keys


# cipher_top: список 5 найчастіших біграм шифртексту (рядки)
def candidates(cipher_top):
    result = []
    seen = set()
    total_pairs = 0
    no_key = 0
    many_keys = 0

    for i in range(len(lang_top)):
        for j in range(i + 1, len(lang_top)):
            X1 = bigram_to_number(lang_top[i])
            X2 = bigram_to_number(lang_top[j])

            for p in range(len(cipher_top)):
                for q in range(len(cipher_top)):
                    if p == q:
                        continue
                    Y1 = bigram_to_number(cipher_top[p])
                    Y2 = bigram_to_number(cipher_top[q])

                    keys = find_keys(X1, Y1, X2, Y2)
                    total_pairs += 1
                    if len(keys) == 0:
                        no_key += 1
                    if len(keys) > 1:
                        many_keys += 1

                    descr = (
                        lang_top[i]
                        + "->"
                        + cipher_top[p]
                        + ", "
                        + lang_top[j]
                        + "->"
                        + cipher_top[q]
                    )
                    for key in keys:
                        if key not in seen:
                            seen.add(key)
                            result.append((key[0], key[1], descr))

    stats = (total_pairs, no_key, many_keys)
    return result, stats


if __name__ == "__main__":

    # ------------------------- ЗАВДАННЯ 1 -------------------------
    print("\n                 >>> ЗАВДАННЯ 1 <<<\n")

    print("1. Обчислення оберненого елемента\n")
    a = 12
    u = inverse(a, n)
    print("a =", a)
    print("mod =", n)
    print("a^(-1) =", u, "mod", n)
    if u is not None:
        print("Перевірка:", a, "*", u, "mod", n, "=", (a * u) % n)
    else:
        print("Оберненого елемента не існує")

    print("\n2. Розв'язування лінійних порівнянь\n")

    print("1) з одним розв'язком:")
    a, b, mod = 7, 4, 31
    solutions = solve_linear(a, b, mod)
    print(f"{a}x ≡ {b} (mod {mod})")
    print("Розв'язки:", solutions)
    for x in solutions:
        print("Перевірка:", f"{a}*{x} mod {mod} =", (a * x) % mod)

    print("\n2) з декількома розв'язками:")
    a, b, mod = 10, 20, 25
    solutions = solve_linear(a, b, mod)
    print(f"{a}x ≡ {b} (mod {mod})")
    print("Кількість розв'язків:", len(solutions))
    print("Розв'язки:", solutions)
    for x in solutions:
        print("Перевірка:", f"{a}*{x} mod {mod} =", (a * x) % mod)

    print("\n3) без розв'язків:")
    a, b, mod = 10, 12, 25
    solutions = solve_linear(a, b, mod)
    print(f"{a}x ≡ {b} (mod {mod})")
    if len(solutions) == 0:
        print("Розв'язків немає")
    else:
        print("Розв'язки:", solutions)

    print("\n4) за модулем m² = 961 (як у шифрі):")
    a, b, mod = 31, 93, 961
    solutions = solve_linear(a, b, mod)
    print(f"{a}x ≡ {b} (mod {mod})")
    print("Кількість розв'язків:", len(solutions))
    print("Перші розв'язки:", solutions[:5])

    # ------------------------- ЗАВДАННЯ 2 -------------------------
    print("\n                 >>> ЗАВДАННЯ 2 <<<\n")

    # Зчитування файлу "05.txt" строго з поточного каталогу
    raw = open("05.txt", "rb").read()
    try:
        cipher_text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        cipher_text = raw.decode("cp1251")

    cipher = "".join([c for c in cipher_text.lower() if c in alphabet])

    print("Довжина шифртексту:", len(cipher))

    top, total = top_bigrams(cipher)
    cipher_top = [bg for bg, cnt in top]
    print("Всього біграм:", total)
    print("\n5 найчастіших біграм:")
    for bg, cnt in top:
        print(
            f"{bg}: {cnt} шт, частота = {cnt / total:.5f} ({cnt / total * 100:.2f} %)"
        )

    # ------------------------- ЗАВДАННЯ 3 -------------------------
    print("\n                 >>> ЗАВДАННЯ 3 <<<\n")

    keys, stats = candidates(cipher_top)

    print("Найчастіші біграми російської мови:", lang_top)
    print("Найчастіші біграми шифртексту:", cipher_top)

    print("\nПеревірено зіставлень:", stats[0])
    print("Зіставлень без жодного ключа:", stats[1])
    print("Зіставлень з кількома ключами:", stats[2])
    print("Унікальних кандидатів (a, b):", len(keys))
    print("\nПерші 10 кандидатів на ключ:")
    for a, b, descr in keys[:10]:
        print("a =", a, "b =", b, "(", descr, ")")

    with open("candidates.txt", "w", encoding="utf-8") as out:
        for a, b, descr in keys:
            out.write(f"({a}, {b}) # {descr}\n")

    print("\nУсі кандидати записані у candidates.txt")
