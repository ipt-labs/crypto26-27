from collections import Counter
from itertools import combinations, permutations
from math import gcd
from pathlib import Path


# У варіанті 5 літера «ь» стоїть перед «ы».
ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя"
MODULUS = len(ALPHABET) ** 2
COMMON_BIGRAMS = ("ст", "но", "то", "на", "ен")


def mod_inverse(a, modulus):
    previous_r, r = modulus, a % modulus
    previous_t, t = 0, 1

    # Кожна остача задовольняє r ≡ t * a (mod modulus).
    while r:
        quotient, remainder = divmod(previous_r, r)
        previous_r, r = r, remainder
        previous_t, t = t, previous_t - quotient * t

    if previous_r != 1:
        return None
    return previous_t % modulus


def solve_congruence(a, b, modulus):
    divisor = gcd(a, modulus)
    if b % divisor:
        return []

    reduced_modulus = modulus // divisor
    inverse = mod_inverse(a // divisor, reduced_modulus)
    first_solution = (inverse * (b // divisor)) % reduced_modulus
    return [first_solution + k * reduced_modulus for k in range(divisor)]


def split_bigrams(text):
    for i in range(0, len(text) - 1, 2):
        yield text[i:i + 2]


def bigram_number(bigram):
    first, second = bigram
    return ALPHABET.index(first) * len(ALPHABET) + ALPHABET.index(second)


def find_candidate_keys(cipher_bigrams):
    plain_numbers = [bigram_number(bigram) for bigram in COMMON_BIGRAMS]
    cipher_numbers = [bigram_number(bigram) for bigram in cipher_bigrams]
    keys = set()

    for x1, x2 in combinations(plain_numbers, 2):
        for y1, y2 in permutations(cipher_numbers, 2):
            for a in solve_congruence(x1 - x2, y1 - y2, MODULUS):
                if gcd(a, MODULUS) == 1:
                    b = (y1 - a * x1) % MODULUS
                    keys.add((a, b))

    return keys


def decrypt(cipher_numbers, a, b):
    inverse = mod_inverse(a, MODULUS)
    bigrams = []
    for y in cipher_numbers:
        x = inverse * (y - b) % MODULUS
        first, second = divmod(x, len(ALPHABET))
        bigrams.append(ALPHABET[first] + ALPHABET[second])
    return "".join(bigrams)


def trigrams(text):
    return (text[i:i + 3] for i in range(len(text) - 2))


def language_score(text, common_trigrams):
    matches = sum(trigram in common_trigrams for trigram in trigrams(text))
    return matches / (len(text) - 2)


def main():
    ciphertext = "".join(Path("05.txt").read_text(encoding="utf-8").split())
    cipher_bigrams = list(split_bigrams(ciphertext))
    counts = Counter(cipher_bigrams)
    top_bigrams = counts.most_common(5)

    print(f"Кількість біграм: {len(cipher_bigrams)}")
    for bigram, count in top_bigrams:
        print(f"{bigram}: {count}, частота {count / len(cipher_bigrams):.2%}")

    keys = find_candidate_keys([bigram for bigram, _ in top_bigrams])
    cipher_numbers = [bigram_number(bigram) for bigram in cipher_bigrams]
    print(f"Кількість кандидатів на ключ: {len(keys)}")

    corpus_path = Path("../../lab1/ФБ-43_Бойко_Бурлачка/text_without_spaces.txt")
    corpus = "".join(corpus_path.read_text(encoding="utf-8").split()).replace("ъ", "ь")
    trigram_counts = Counter(trigrams(corpus))
    common_trigrams = {trigram for trigram, _ in trigram_counts.most_common(30)}

    results = []
    for a, b in keys:
        plaintext = decrypt(cipher_numbers, a, b)
        score = language_score(plaintext, common_trigrams)
        results.append((score, (a, b), plaintext))

    results.sort(reverse=True)
    for score, key, plaintext in results[:3]:
        print(f"Ключ {key}, частка частих триграм {score:.2%}")
        print(plaintext[:100])

    _, _, best_plaintext = results[0]
    Path("decrypted.txt").write_text(best_plaintext + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
