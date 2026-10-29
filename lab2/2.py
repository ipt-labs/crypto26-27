import matplotlib.pyplot as plt
ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"  
M = len(ALPHABET)
IDX = {c: i for i, c in enumerate(ALPHABET)}
def clean(text):
    text = text.lower().replace("ё", "е")
    return "".join(c for c in text if c in IDX)
def index_of_coincidence(text):
    n = len(text)
    if n < 2:
        return 0.0
    counts = [0] * M
    for c in text:
        counts[IDX[c]] += 1
    return sum(k * (k - 1) for k in counts) / (n * (n - 1))
def avg_ic(text, r):
    blocks = [text[i::r] for i in range(r)]
    return sum(index_of_coincidence(b) for b in blocks) / r
def d_stat(text, r):
    return sum(1 for i in range(len(text) - r) if text[i] == text[i + r])
with open("v3.txt", encoding="utf-8", errors="ignore") as f:
    y = clean(f.read())
print("Довжина шифртексту:", len(y))
print("-" * 28)
print(f"{'r':>3} | {'Середній IC':>11} | {'D_r':>6}")
print("-" * 28)

R_MAX = 35
rs = list(range(2, R_MAX + 1))
ics = [avg_ic(y, r) for r in rs]
ds = [d_stat(y, r) for r in rs]

for r, ic, d in zip(rs, ics, ds):
    marker = "<-- сплеск!" if ic > 0.045 else ""
    print(f"{r:>3} | {ic:>11.5f} | {d:>6} {marker}")

fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].bar(rs, ics)
ax[0].set_title("Середній IC блоків")
ax[0].set_xlabel("r")

ax[1].bar(rs, ds)
ax[1].set_title("Статистика D_r")
ax[1].set_xlabel("r")

plt.tight_layout()
plt.show()