import math

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
m = len(alphabet)
n = m * m


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


def inverse(a, mod):
    d, u, v = egcd(a % mod, mod)
    return u % mod if d == 1 else None


def bigram_to_number(bg):
    return alphabet.index(bg[0]) * m + alphabet.index(bg[1])


def number_to_bigram(X):
    return alphabet[X // m] + alphabet[X % m]


def affine_decrypt(text, a, b):
    a_inv = inverse(a, n)
    res = []
    for i in range(0, len(text) - 1, 2):
        Y = bigram_to_number(text[i:i + 2])
        res.append(number_to_bigram((a_inv * (Y - b)) % n))
    return "".join(res)


# ---------- Автоматичний розпізнавач (завдання 4) ----------
FORBIDDEN = ["ьь", "ыы", "ыь", "ьы", "йь", "йы",
             "аь", "оь", "еь", "иь", "уь", "эь", "юь", "яь"]

FREQ = {
    'о': .110, 'е': .085, 'а': .080, 'и': .074, 'н': .067, 'т': .063,
    'с': .055, 'р': .047, 'в': .045, 'л': .044, 'к': .035, 'м': .032,
    'д': .030, 'п': .028, 'у': .026, 'я': .020, 'ы': .019, 'ь': .019,
    'г': .017, 'з': .016, 'б': .016, 'ч': .014, 'й': .012, 'х': .009,
    'ж': .007, 'ш': .007, 'ю': .006, 'ц': .004, 'щ': .003, 'э': .003,
    'ф': .002,
}

FORBIDDEN_MAX = 0.002
SCORE_MIN = -3.3


def forbidden_rate(text):
    cnt = sum(1 for i in range(len(text) - 1) if text[i:i + 2] in FORBIDDEN)
    return cnt / max(1, len(text) - 1)


def letter_score(text):
    return sum(math.log(FREQ[c]) for c in text) / len(text)


def is_meaningful(text):
    return forbidden_rate(text) <= FORBIDDEN_MAX and letter_score(text) >= SCORE_MIN


if __name__ == "__main__":
    raw = open("05.txt", "rb").read()
    try:
        cipher = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        cipher = raw.decode("cp1251")
    cipher = "".join(c for c in cipher.lower() if c in alphabet)

    keys = []
    with open("candidates.txt", encoding="utf-8-sig") as f:
        for line in f:
            part = line.split("#")[0].strip()
            if not part:
                continue
            a_s, b_s = part.strip("()").split(",")
            keys.append((int(a_s), int(b_s)))

    # Завдання 4: дешифруємо кожного, відкидаємо безглуздих
    good = []
    for a, b in keys:
        if inverse(a, n) is None:
            continue
        dec = affine_decrypt(cipher, a, b)
        if is_meaningful(dec):
            good.append((letter_score(dec), a, b, dec))
    good.sort(reverse=True)

    print(f"Кандидатів: {len(keys)}, відкинуто: {len(keys) - len(good)}, "
          f"лишилось: {len(good)}")

    # Завдання 5: лишився змістовний текст
    if good:
        sc, a, b, dec = good[0]
        print(f"Ключ: a={a}, b={b}, score={sc:.3f}")
        print(dec[:300])
        with open("decrypted_05.txt", "w", encoding="utf-8") as out:
            out.write(dec)
    else:
        print("Жоден кандидат не пройшов розпізнавач.")
