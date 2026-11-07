"""Статистичні характеристики тексту для криптоаналізу шифру Віженера."""

from collections import Counter
from typing import List


def calc_ic(text: str) -> float:
    """I = sum(n_i * (n_i - 1)) / (N * (N - 1))."""
    n = len(text)
    if n < 2:
        return 0.0
    counts = Counter(text)
    return sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))


def calc_dr(text: str, r: int) -> int:
    """Кількість збігів символів на відстані r."""
    if r <= 0:
        raise ValueError("Відстань r має бути додатною.")
    if r >= len(text):
        return 0
    return sum(text[i] == text[i + r] for i in range(len(text) - r))


def get_blocks(text: str, r: int) -> List[str]:
    """Розбиття на r блоків: Y0=text[0::r], Y1=text[1::r], ..."""
    if r <= 0:
        raise ValueError("Довжина ключа r має бути додатною.")
    return [text[i::r] for i in range(r)]


def avg_ic_for_r(text: str, r: int) -> float:
    """Середнє арифметичне IC усіх r блоків."""
    blocks = get_blocks(text, r)
    values = [calc_ic(block) for block in blocks if len(block) > 1]
    return sum(values) / len(values) if values else 0.0
