import collections

with open("text_5.txt", "r", encoding="utf-8") as file:
    text = file.read()

text = text.lower().replace('ё', 'е')

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

text = ''.join([x for x in text if x in ALPHABET])

def calc_ic(text):
    N = len(text)
    if N <= 1:
        return 0.0
    
    counts = collections.Counter(text)

    chyselnyk = 0
    for c in counts.values():
        chyselnyk += c * (c - 1)

    znamennyk = N * (N - 1)

    return chyselnyk / znamennyk


ic_value = calc_ic(text)
print("Індекс відповідності нашого  тексту:", ic_value)


def get_avg_ic(text, r):
    columns_ic = [calc_ic(text[i::r]) for i in range(r)]
    return sum(columns_ic) / r

def get_d_r(text, r):
    return sum(1 for i in range(len(text) - r) if text[i] == text[i + r])

print(f"{'r':<4} | {'Середній ІК':<15} | {'D_r':<10}")
print("-" * 35)

for r in range(1, 31):
    avg_ic = get_avg_ic(text, r)
    d_r = get_d_r(text, r)

    mark = " <--- Скоріше за все це наш період" if avg_ic > 0.05 else ""
    print(f"{r:<4} | {avg_ic:<15.5f} | {d_r:<10}{mark}")