from collections import Counter

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
CORPUS_PATH = "../../lab1/ФБ-43_Коротка_Тимчак/corpus.txt"
PLAINTEXT_PATH = "plaintext.txt"
CIPHERTEXT_PATH = "ciphertext_v4.txt"
DECRYPTED_PATH = "decrypted_v4.txt"
RESULTS_PATH = "results.txt"

KEYS = ["да", "кот", "шифр", "лампа", "защитаинформации"]
MAX_R = 30
ERROR_POS = 5  # позиція символу ключа, який псуємо в частині 4
# Блоки, де найчастіша літера шифртексту відповідає не «о», а іншій
# імовірній літері мови; обрано вручну за читабельністю розшифрування
X_STAR_FIX = {4: "а", 6: "а", 8: "е", 10: "е"}


def normalize(text):
    text = text.lower().replace("ё", "е")
    return "".join(ch for ch in text if ch in ALPHABET)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def letter_probs(text):
    cnt = Counter(text)
    return {a: cnt[a] / len(text) for a in ALPHABET}


def shift(text, key, sign):
    idx = [ALPHABET.index(k) for k in key]
    r = len(key)
    return "".join(
        ALPHABET[(ALPHABET.index(ch) + sign * idx[i % r]) % M]
        for i, ch in enumerate(text)
    )


def encrypt(text, key):
    return shift(text, key, 1)


def decrypt(text, key):
    return shift(text, key, -1)


def index_of_coincidence(text):
    n = len(text)
    return sum(c * (c - 1) for c in Counter(text).values()) / (n * (n - 1))


def blocks(text, r):
    return [text[i::r] for i in range(r)]


def avg_block_ic(text, r):
    return sum(index_of_coincidence(b) for b in blocks(text, r)) / r


def coincidences(text, r):
    return sum(text[i] == text[i + r] for i in range(len(text) - r))


def key_letter(y_star, x_star):
    # k = (y* - x*) mod m
    return ALPHABET[(ALPHABET.index(y_star) - ALPHABET.index(x_star)) % M]


def key_by_top_letter(text, r, x_star="о", fix=None):
    fix = fix or {}
    key = ""
    for i, b in enumerate(blocks(text, r)):
        y_star = Counter(b).most_common(1)[0][0]
        key += key_letter(y_star, fix.get(i, x_star))
    return key


out = []


def w(s=""):
    out.append(s)
    print(s)


def main():
    corpus = normalize(read(CORPUS_PATH))
    probs = letter_probs(corpus)
    i_theor = sum(p * p for p in probs.values())
    i0 = 1 / M
    top_lang = sorted(ALPHABET, key=lambda a: -probs[a])

    w(f"Теоретичний індекс відповідності мови I = {i_theor:.4f}, I0 = 1/m = {i0:.4f}")
    w(f"Найчастіші літери мови: {', '.join(top_lang[:5])}")
    w()

    # 1. Дослідження шифру Віженера
    plain = normalize(read(PLAINTEXT_PATH))
    n = len(plain)
    w("1. ДОСЛІДЖЕННЯ ШИФРУ ВІЖЕНЕРА")
    w(f"Довжина відкритого тексту: {n} літер")
    w(f"{'Текст':<24}{'r':>3}{'I(Y)':>9}")
    w(f"{'відкритий текст':<24}{'-':>3}{index_of_coincidence(plain):>9.4f}")
    for key in KEYS:
        y = encrypt(plain, key)
        assert decrypt(y, key) == plain
        w(f"{'ключ ' + key:<24}{len(key):>3}{index_of_coincidence(y):>9.4f}")
    w()

    # 2. Криптоаналіз шифртексту
    cipher = normalize(read(CIPHERTEXT_PATH))
    w("2. КРИПТОАНАЛІЗ ШИФРТЕКСТУ (варіант 4)")
    w(f"Довжина шифртексту: {len(cipher)} літер, I(Y) = {index_of_coincidence(cipher):.4f}")
    w(f"{'r':>3}{'сер. I блоків':>15}{'D_r':>7}")
    stats = {}
    for r in range(1, MAX_R + 1):
        stats[r] = (avg_block_ic(cipher, r), coincidences(cipher, r))
        w(f"{r:>3}{stats[r][0]:>15.4f}{stats[r][1]:>7}")
    best_r = max(range(2, MAX_R + 1), key=lambda r: stats[r][0])
    w(f"Найбільш імовірний період: r = {best_r}")
    w()

    multiples = [r for r in range(2 * best_r, MAX_R + 1, best_r)]
    noise = sorted(
        (r for r in range(2, MAX_R + 1) if r % best_r),
        key=lambda r: -stats[r][1],
    )[:2]
    w("Альтернативні кандидати:")
    for r in multiples + noise:
        key = key_by_top_letter(cipher, r)
        w(f"  r = {r}: сер. I = {stats[r][0]:.4f}, D_r = {stats[r][1]}, ключ -> {key}")
    w()

    # 3. Відновлення ключа та відкритого тексту
    r = best_r
    w("3. ВІДНОВЛЕННЯ КЛЮЧА")
    w(f"{'i':>3}{'y*':>4}{'N(y*)':>7}{'k (x*=о)':>10}{'k (x*=е)':>10}{'k (x*=а)':>10}")
    for i, b in enumerate(blocks(cipher, r)):
        y_star, cnt = Counter(b).most_common(1)[0]
        ks = [key_letter(y_star, x) for x in "оеа"]
        w(f"{i:>3}{y_star:>4}{cnt:>7}{ks[0]:>10}{ks[1]:>10}{ks[2]:>10}")
    key_simple = key_by_top_letter(cipher, r)
    w(f"Ключ при x* = о для всіх блоків: {key_simple}")
    w(f"Розшифрування: {decrypt(cipher, key_simple)[:78]}")
    key = key_by_top_letter(cipher, r, fix=X_STAR_FIX)
    w(f"Виправлені блоки: {X_STAR_FIX}")
    w(f"Ключ після виправлення: {key}")
    w()

    plain_v4 = decrypt(cipher, key)
    with open(DECRYPTED_PATH, "w", encoding="utf-8") as f:
        f.write(plain_v4 + "\n")
    w(f"I(розшифрованого тексту) = {index_of_coincidence(plain_v4):.4f}")
    w(f"Початок розшифрування: {plain_v4[:200]}")
    w()

    # 4. Вплив помилки у ключі
    wrong = list(key)
    wrong[ERROR_POS] = ALPHABET[(ALPHABET.index(wrong[ERROR_POS]) + 1) % M]
    wrong = "".join(wrong)
    plain_wrong = decrypt(cipher, wrong)
    diff = [i for i in range(len(cipher)) if plain_v4[i] != plain_wrong[i]]
    w("4. ПОМИЛКА У КЛЮЧІ")
    w(f"Правильний ключ: {key}, зіпсований: {wrong} (позиція {ERROR_POS})")
    w(f"Змінено літер: {len(diff)} з {len(cipher)}")
    w(f"Усі змінені позиції ≡ {ERROR_POS} (mod {r}): {all(i % r == ERROR_POS for i in diff)}")
    w(f"Правильно:   {plain_v4[:78]}")
    w(f"З помилкою:  {plain_wrong[:78]}")

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
