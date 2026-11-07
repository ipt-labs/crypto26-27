"""Пошук періоду та відновлення ключа за частотами з КП №1."""

from collections import Counter
from typing import List, Tuple

from .vigenere import M, CHAR_TO_IDX, IDX_TO_CHAR
from .stats import avg_ic_for_r, calc_dr, get_blocks

# Частоти отримані з characters_without_spaces.csv у КП №1.
# У КП №1 літера ё була окремою, а в КП №2 використовується алфавіт без ё.
# Тому count(ё) додано до count(е), після чого частоти нормовано.
RUS_FREQS = {
    "а": 0.0823091960, "б": 0.0177930887, "в": 0.0453203921,
    "г": 0.0197020883, "д": 0.0303998933, "е": 0.0824203018,
    "ж": 0.0104197038, "з": 0.0169985139, "и": 0.0662904333,
    "й": 0.0115846313, "к": 0.0345922855, "л": 0.0507255209,
    "м": 0.0298867866, "н": 0.0657207635, "о": 0.1144120382,
    "п": 0.0259570081, "р": 0.0444746413, "с": 0.0525853646,
    "т": 0.0580888052, "у": 0.0278155051, "ф": 0.0019675827,
    "х": 0.0086548051, "ц": 0.0035681796, "ч": 0.0145669803,
    "ш": 0.0092500628, "щ": 0.0028476753, "ъ": 0.0004417297,
    "ы": 0.0193364492, "ь": 0.0198583098, "э": 0.0031951334,
    "ю": 0.0063761261, "я": 0.0224400046,
}


def find_possible_periods(text: str, max_r: int = 30) -> List[Tuple[int, float, int]]:
    """Повертає (r, середній IC, D_r) для всіх r від 2 до max_r."""
    return [
        (r, avg_ic_for_r(text, r), calc_dr(text, r))
        for r in range(2, min(max_r, len(text) - 1) + 1)
    ]


def recover_key_chisquare(text: str, r: int) -> str:
    """Підбирає кожен символ ключа за мінімумом критерію хі-квадрат."""
    blocks = get_blocks(text, r)
    key = []

    for block in blocks:
        n = len(block)
        if n == 0:
            raise ValueError("Недостатньо символів шифртексту для такого періоду.")
        observed_counts = Counter(CHAR_TO_IDX[ch] for ch in block)
        best_shift = 0
        min_chisq = float("inf")

        for shift in range(M):
            chisq = 0.0
            for char, probability in RUS_FREQS.items():
                expected = n * probability
                observed = observed_counts.get(
                    (CHAR_TO_IDX[char] + shift) % M, 0
                )
                chisq += (observed - expected) ** 2 / expected
            if chisq < min_chisq:
                min_chisq = chisq
                best_shift = shift

        key.append(IDX_TO_CHAR[best_shift])

    return "".join(key)


def recover_key(text: str, r: int, target_char: str = "о") -> str:
    """Наївний метод: найчастішу літеру блоку вважаємо заданою target_char."""
    if target_char not in CHAR_TO_IDX:
        raise ValueError("target_char має бути літерою робочого алфавіту.")
    key = []
    target_idx = CHAR_TO_IDX[target_char]
    for block in get_blocks(text, r):
        if not block:
            raise ValueError("Недостатньо символів шифртексту.")
        y = Counter(block).most_common(1)[0][0]
        key_idx = (CHAR_TO_IDX[y] - target_idx) % M
        key.append(IDX_TO_CHAR[key_idx])
    return "".join(key)
