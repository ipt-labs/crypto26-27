import math
import re
import random
from collections import Counter


RUSSIAN_LETTERS = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_WITH_SPACE = set(RUSSIAN_LETTERS + " ")

def preprocess(raw_text: str, keep_spaces: bool = True) -> str:
    text = raw_text.lower()
    text = text.replace("ё", "е")
    text = "".join(ch if ch in ALPHABET_WITH_SPACE else " " for ch in text)
    text = re.sub(r" +", " ", text).strip()
    if not keep_spaces:
        text = text.replace(" ", "")
        
    return text
file_name = "БратьяКарамазовы_Достоевский.txt"

with open(file_name, encoding="utf-8", errors="ignore") as f:
    raw_data = f.read()

print("Довжина сирого тексту:", len(raw_data))

text_with_spaces = preprocess(raw_data, keep_spaces=True)
text_no_spaces = preprocess(raw_data, keep_spaces=False)

print("Довжина після нормалізації (з пробілами):", len(text_with_spaces))
print("Довжина без пробілів:", len(text_no_spaces))
print("\nПерші 300 символів нормалізованого тексту (з пробілами):")
print(text_with_spaces[:300])



def calc_entropy(counts: Counter, total: int) -> float:
    h = 0.0
    for c in counts.values():
        p = c / total
        h -= p * math.log2(p)
    return h

def analyze_text(text: str, is_spaced: bool):
    total = len(text)
    counts = Counter(text)
    h1 = calc_entropy(counts, total)

    bg_over = [text[i:i+2] for i in range(total - 1)]
    h2_over = calc_entropy(Counter(bg_over), len(bg_over)) / 2.0

    bg_nonover = [text[i:i+2] for i in range(0, total - 1, 2)]
    h2_nonover = calc_entropy(Counter(bg_nonover), len(bg_nonover)) / 2.0

    label = "ТЕКСТ З ПРОБІЛОМ" if is_spaced else "ТЕКСТ БЕЗ ПРОБІЛІВ"
    alpha_size = 33 if is_spaced else 32

    print("=" * 60)
    print(f"{label} (алфавіт із {alpha_size} символів)")
    print("=" * 60)
    
    print("Топ-5 символів (символ, кількість, частка):")
    for ch, n in counts.most_common(5):
        display_ch = "'пробіл'" if ch == " " else f"'{ch}'"
        print(f"{display_ch:>15} {n:>10} {n/total:>8.4f}")
        
    print("Топ-5 біграм, що ПЕРЕТИНАЮТЬСЯ:")
    for bg, n in Counter(bg_over).most_common(5):
        display_bg = f"'{bg}'"
        print(f"{display_bg:>15} {n:>10} {n/len(bg_over):>8.4f}")
        
    print("Топ-5 біграм, що НЕ перетинаються:")
    for bg, n in Counter(bg_nonover).most_common(5):
        display_bg = f"'{bg}'"
        print(f"{display_bg:>15} {n:>10} {n/len(bg_nonover):>8.4f}")

    print(f"{'H1':<15} = {h1:.4f} біт/симв.")
    print(f"{'H2 (перетин.)':<15} = {h2_over:.4f} біт/симв.")
    print(f"{'H2 (без перет.)':<15} = {h2_nonover:.4f} біт/симв.")
    print("\n")

analyze_text(text_with_spaces, True)
analyze_text(text_no_spaces, False)
SEQ_LENGTH = 20000
seq_a = text_no_spaces[:SEQ_LENGTH]

most_common_char = Counter(text_no_spaces).most_common(1)[0][0]
seq_b = most_common_char * SEQ_LENGTH

alphabet = sorted(list(set(text_no_spaces))) 

rng = random.Random(42) 
seq_v = "".join(rng.choice(alphabet) for _ in range(SEQ_LENGTH))

print("=" * 60)
print("ЕТАП 3: ДОСЛІДЖЕННЯ ВПЛИВУ РОЗПОДІЛУ СИМВОЛІВ")
print("=" * 60)

for name, seq in [("А (Природний текст)", seq_a), 
                  ("Б (Один символ)", seq_b), 
                  ("В (Рівноймовірна)", seq_v)]:
    counts = Counter(seq)
    h1 = calc_entropy(counts, len(seq))
    print(f"Послідовність {name}:")
    print(f"  Довжина: {len(seq)}")
    print(f"  Унікальних символів: {len(counts)}")
    print(f"  H1 = {h1:.4f} біт/символ\n")




    base_chars = list(text_no_spaces[:SEQ_LENGTH])


random.seed(42) 
random.shuffle(base_chars)
seq_g = "".join(base_chars)


counts = Counter(text_no_spaces[:SEQ_LENGTH])
symbols_sorted = sorted(counts.keys())
remaining = dict(counts)
pattern = []


while sum(remaining.values()) > 0:
    for s in symbols_sorted:
        if remaining.get(s, 0) > 0:
            pattern.append(s)
            remaining[s] -= 1
seq_d = "".join(pattern)

print("=" * 60)
print("ЕТАП 4: ДОСЛІДЖЕННЯ ЗАЛЕЖНОСТЕЙ МІЖ СИМВОЛАМИ")
print("=" * 60)

for name, seq in [("Г (Випадковий порядок)", seq_g), ("Д (Періодична структура)", seq_d)]:
    h1 = calc_entropy(Counter(seq), len(seq))
    
    bg_over = [seq[i:i+2] for i in range(len(seq) - 1)]
    h2_over = calc_entropy(Counter(bg_over), len(bg_over)) / 2.0
    
    bg_nonover = [seq[i:i+2] for i in range(0, len(seq) - 1, 2)]
    h2_nonover = calc_entropy(Counter(bg_nonover), len(bg_nonover)) / 2.0
    
    print(f"Послідовність {name}:")
    print(f"  H1 = {h1:.4f} біт/символ")
    print(f"  H2 (перекривні) = {h2_over:.4f} біт/символ")
    print(f"  H2 (неперекривні) = {h2_nonover:.4f} біт/символ\n")