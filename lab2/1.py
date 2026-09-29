ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
IDX = {c: i for i, c in enumerate(ALPHABET)}

FREQ = {
    'о': 0.1097, 'е': 0.0845, 'а': 0.0801, 'и': 0.0735, 'н': 0.0670,
    'т': 0.0626, 'с': 0.0547, 'р': 0.0473, 'в': 0.0454, 'л': 0.0440,
    'к': 0.0349, 'м': 0.0321, 'д': 0.0298, 'п': 0.0281, 'у': 0.0262,
    'я': 0.0201, 'ы': 0.0190, 'ь': 0.0174, 'г': 0.0170, 'з': 0.0165,
    'б': 0.0159, 'ч': 0.0144, 'й': 0.0121, 'х': 0.0097, 'ж': 0.0094,
    'ш': 0.0073, 'ю': 0.0064, 'ц': 0.0048, 'щ': 0.0036, 'э': 0.0032,
    'ф': 0.0026, 'ъ': 0.0004,
}

def clean(text):
    text = text.lower().replace("ё", "е")
    return "".join(c for c in text if c in IDX)

def load(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        return clean(f.read())

def encrypt(text, key):
    r = len(key)
    return "".join(ALPHABET[(IDX[c] + IDX[key[i % r]]) % M] for i, c in enumerate(text))

def index_of_coincidence(text):
    n = len(text)
    if n < 2:
        return 0.0
    counts = [0] * M
    for c in text:
        counts[IDX[c]] += 1
    return sum(k * (k - 1) for k in counts) / (n * (n - 1))

def theoretical_ic():
    s = sum(FREQ.values())
    return sum((p / s) ** 2 for p in FREQ.values())

print("Завантаження та обробка тексту...")
full_text = load("voina_i_mir.txt")
plain = full_text[:3000] 
print("Довжина відкритого тексту:", len(plain), "символів (~3 КБ)")
print("Теоретичний IC російської мови:", round(theoretical_ic(), 5))
print("IC відкритого тексту:", round(index_of_coincidence(plain), 5))
print("-" * 45)

keys = [
    "он",                 # r = 2
    "она",                # r = 3
    "боль",               # r = 4
    "война",              # r = 5
    "левниколаевичтолстой",   # r = 20 
]

print(f"{'r':>3} | {'Ключ':<18} | {'IC шифртексту':<15}")
print("-" * 45)

for key in sorted(keys, key=len):
    enc = encrypt(plain, key)
    ic_val = index_of_coincidence(enc)
    print(f"{len(key):>3} | {key:<18} | {ic_val:.5f}")

print("-" * 45)
print("IC для рівноімовірного алфавіту (1/32) =", round(1 / M, 5))