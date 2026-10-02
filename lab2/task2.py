"""
Визначення періоду шифру Віженера:
  1) середній індекс відповідності блоків;
  2) кількість збігів символів на відстані r (D_r).
Використання:  python vigenere_period_finder.py 6var.txt [макс_r]
"""
import sys
from collections import Counter
from statistics import median

LETTERS = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPHA_SET = set(LETTERS)
# Теоретичний IC російської мови. Замініть на значення з ЛР1, якщо воно відрізняється.
THEORY_IC = 0.0558


def load_ciphertext(path):
    with open(path, encoding="utf-8", errors="ignore") as fh:
        raw = fh.read().lower().replace("ё", "е")
    return [ch for ch in raw if ch in ALPHA_SET]


def coincidence_index(seq):
    n = len(seq)
    if n < 2:
        return 0.0
    freq = Counter(seq)
    return sum(v * (v - 1) for v in freq.values()) / (n * (n - 1))


def mean_block_ic(seq, period):
    parts = (seq[k::period] for k in range(period))
    return sum(map(coincidence_index, parts)) / period


def shifted_matches(seq, shift):
    return sum(a == b for a, b in zip(seq, seq[shift:]))


def outliers(values, k=5.0):
    """Індекси значень, що значно перевищують медіану (медіана + k * MAD)."""
    med = median(values)
    mad = median(abs(v - med) for v in values) or 1e-12
    return {i for i, v in enumerate(values) if (v - med) / mad > k}


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "6var.txt"
    r_max = int(sys.argv[2]) if len(sys.argv) > 2 else 40

    text = load_ciphertext(path)
    n = len(text)
    rs = list(range(2, r_max + 1))
    ics = [mean_block_ic(text, r) for r in rs]
    dss = [shifted_matches(text, r) for r in rs]
    marked = outliers(ics) & outliers(dss)

    print(f"n = {n}, IC шифртексту = {coincidence_index(text):.5f}, "
          f"для випадкового тексту: IC = {1/32:.5f}, D_r ~ {n/32:.0f}\n")
    print("  r   сер. IC     D_r")
    for i, r in enumerate(rs):
        print(f"{r:>3}  {ics[i]:.5f}  {dss[i]:>5}{'  *' if i in marked else ''}")

    cands = [rs[i] for i in sorted(marked)]
    if not cands:
        print("\nВиділених значень немає - збільште r_max.")
        return
    r0 = cands[0]
    print(f"\n* - виділені значення в обох методах: {cands}")

    # --- альтернативні кандидати ---
    print(f"\nАльтернативні кандидати (основний r = {r0}):")
    for c in cands[1:]:
        i = rs.index(c)
        print(f"  r = {c}: кратне {r0} ({c}={c // r0}*{r0}), IC = {ics[i]:.5f}, "
              f"D_r = {dss[i]} -> відкидаємо, істинний період - найменший")
    for d in range(1, r0):
        if r0 % d == 0:
            ic_d = mean_block_ic(text, d)
            print(f"  r = {d}: дільник {r0}, IC = {ic_d:.5f} "
                  f"(далеко від {THEORY_IC}) -> відкидаємо")
    rest = sorted((i for i in range(len(rs)) if i not in marked and rs[i] % r0),
                  key=lambda i: -dss[i])[:3]
    for i in rest:
        print(f"  r = {rs[i]}: найбільший D_r серед решти ({dss[i]}), "
              f"IC = {ics[i]:.5f} ~ {1/32:.3f} -> випадкове коливання, відкидаємо")

    # --- перевірка вибраного r за окремими блоками ---
    blocks = [coincidence_index(text[k::r0]) for k in range(r0)]
    print(f"\nIC окремих блоків для r = {r0} (теорія ~ {THEORY_IC}):")
    print("  " + " ".join(f"{b:.3f}" for b in blocks))
    print(f"  min = {min(blocks):.3f}, max = {max(blocks):.3f}")
    # --- порівняння з теоретично очікуваними значеннями ---
    i0 = rs.index(r0)
    print(f"\nПорівняння для r = {r0} з очікуваним:")
    print(f"  сер. IC блоків: спостережено {ics[i0]:.5f}, очікувано для мови ~ {THEORY_IC}, "
          f"для хибного r ~ {1/32:.5f}")
    exp_true = (n - r0) * THEORY_IC
    print(f"  D_r: спостережено {dss[i0]}, очікувано для істинного r ~ {exp_true:.0f}, "
          f"для хибного r ~ {n/32:.0f}")

    # --- другий алгоритм: IC всього тексту порівнюємо з очікуваним для періоду r ---
    # I(r) ~ IC_мови / r + (1 - 1/r) / 32
    ic_all = coincidence_index(text)
    print(f"\nДругий алгоритм: IC всього тексту = {ic_all:.5f}")
    print("  r    очікуваний IC   |різниця|")
    near = sorted(rs, key=lambda r: abs(THEORY_IC / r + (1 - 1 / r) / 32 - ic_all))[:3]
    for r in [2, 3, 4, 5, r0] + [x for x in near if x not in (2, 3, 4, 5, r0)]:
        e = THEORY_IC / r + (1 - 1 / r) / 32
        print(f"  {r:>2}   {e:.5f}         {abs(e - ic_all):.5f}")
    print("  (для великих r очікувані значення майже не відрізняються - "
          "метод неефективний, див. методичку)")

    print(f"\nВисновок: період ключа r = {r0}")


if __name__ == "__main__":
    main()