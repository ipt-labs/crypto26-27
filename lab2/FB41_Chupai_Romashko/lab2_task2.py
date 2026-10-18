from collections import Counter

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"   
M = len(ALPHABET)
IDX = {ch: i for i, ch in enumerate(ALPHABET)}

R_MAX = 40          # перевіряємо r = 2 ... 40 


def clean_text(raw: str) -> str:
    text = raw.lower().replace("ё", "е")
    return "".join(ch for ch in text if ch in IDX)


def index_of_coincidence(text: str) -> float:
    # I(Y) = 1/(n(n-1)) * sum N_t (N_t - 1)
    n = len(text)
    counts = Counter(text)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))


def language_index(text: str) -> float:
    # теоретичне значення MI = sum p_t^2 за частотами великого тексту
    n = len(text)
    counts = Counter(text)
    return sum((c / n) ** 2 for c in counts.values())


def split_blocks(text: str, r: int) -> list:
    # Y_i = y_i, y_(i+r), y_(i+2r), ...
    return [text[i::r] for i in range(r)]


def average_block_index(text: str, r: int) -> float:
    # Метод 1: середнє значення індексу відповідності по блоках Y_0 ... Y_(r-1)
    indices = [index_of_coincidence(block) for block in split_blocks(text, r)]
    return sum(indices) / len(indices)


def coincidences(text: str, r: int) -> int:
    # Метод 2: D_r = sum delta(y_i, y_(i+r)) - кількість збігів літер на відстані r
    return sum(1 for i in range(len(text) - r) if text[i] == text[i + r])


if __name__ == "__main__":
    with open("variant2.txt", encoding="utf-8", errors="ignore") as f:
        cipher = clean_text(f.read())
    with open("Pyat_lojek_eliksira.txt", encoding="utf-8", errors="ignore") as f:
        I_lang = language_index(clean_text(f.read()))

    n = len(cipher)
    print(f"Довжина шифртексту: {n} літер")
    print(f"Індекс відповідності всього шифртексту: {index_of_coincidence(cipher):.5f}")
    print(f"Теоретичний I мови (частоти з ЛР1):     {I_lang:.5f}")
    print(f"I для рівноймовірного алфавіту (1/m):   {1 / M:.5f}\n")

    print(f"{'r':>3s} {'сер. I блоків':>14s} {'D_r':>7s} {'D_r/(n-r)':>11s}")
    print("-" * 40)
    avg_I, D = {}, {}
    for r in range(2, R_MAX + 1):
        avg_I[r] = average_block_index(cipher, r)
        D[r] = coincidences(cipher, r)
        print(f"{r:3d} {avg_I[r]:14.5f} {D[r]:7d} {D[r] / (n - r):11.5f}")

    top_I = sorted(avg_I, key=avg_I.get, reverse=True)[:5]
    top_D = sorted(D, key=lambda r: D[r] / (n - r), reverse=True)[:5]
    print(f"\nТоп-5 за середнім I блоків: {top_I}")
    print(f"Топ-5 за D_r/(n-r):         {top_D}")

    print("\nІндекси відповідності окремих блоків для найкращих кандидатів:")
    for r in top_I[:3]:
        values = [index_of_coincidence(b) for b in split_blocks(cipher, r)]
        print(f"r = {r}: " + " ".join(f"{v:.3f}" for v in values))