from collections import Counter
alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
m = len(alphabet)  # 32 літер

# читаємо шифртекст
f = open("text_5.txt", "r", encoding="utf-8")
raw_text = f.read().lower().replace("ё", "е")
f.close()

cipher = "".join([char for char in raw_text if char in alphabet])
print("Довжина шифртексту:", len(cipher))

r = 16  # знайдена довжина ключа

# --- ВІДНОВЛЕННЯ КЛЮЧА ---

# розбиваємо шифртекст на r блоків
def get_blocks(text, r):
    blocks = []
    for i in range(r):
        blocks.append(text[i::r])  # літери на позиціях i, i+r, i+2r, ...
    return blocks


blocks = get_blocks(cipher, r)

x_star = "о"  # найімовірніша літера російської мови


# k = (y* - x*) mod m
def get_key_letter(y_star, x_star):
    k = (alphabet.index(y_star) - alphabet.index(x_star)) % m
    return alphabet[k]

# Шукаємо ключ, за X^* беремо найімовірнішу літеру "о"
print()
print("Ключ при x* = 'о':")
key = ""
for i in range(r):
    counts = Counter(blocks[i])
    y_star = counts.most_common(1)[0][0]  # найчастіша літера блоку
    k = get_key_letter(y_star, x_star)
    key += k
    print("Блок", i, ": y* =", y_star, "->", "k =", k)

print()
print("Початковий ключ:", key)

# розшифрування (зворотна дія до розшифрування)
def decrypt(text, key):
    result = ""
    for i in range(len(text)):
        y = alphabet.index(text[i])
        k = alphabet.index(key[i % len(key)])
        result += alphabet[(y - k) % m]
    return result

def calc_ic(text):
    N = len(text)
    if N <= 1:
        return 0.0
    
    counts = Counter(text)

    chyselnyk = 0
    for c in counts.values():
        chyselnyk += c * (c - 1)

    znamennyk = N * (N - 1)

    return chyselnyk / znamennyk


# розшифровуємо фрагмент тексту початковим ключем, щоб знайти неправильні позиції 
plain = decrypt(cipher, key)   # key = "декелисоборойдей"

print()
print("Розшифрування по 16 літер у рядку:")
for start in range(0, 160, r):  # перші 10 рядків
    print(plain[start:start + r])

# беремо наступну за імовірністю букву, щоб знайти правильні літери ключа для позицій 2, 3, 12, 13
x_star = "е"  # друга за імовірністю літера мови
problem_blocks = [2, 3, 12, 13]  # блоки, де ключ вийшов неправильно

print()
print("Кандидати при x* = 'е':")
for i in problem_blocks:
    counts = Counter(blocks[i])
    top = counts.most_common(2)   # дві найчастіші літери (для випадків з нічиєю)

    parts = []
    for c, cnt in top:
        k = get_key_letter(c, x_star)
        parts.append(c + "(" + str(cnt) + ") -> " + k)

    print("Блок", i, ":", "; ".join(parts))

# виправляємо неправильні літери на позиціях 2, 3, 12, 13
fix = {2: "л", 3: "о", 12: "т", 13: "н"}
key_list = list(key)
for i in fix:
    key_list[i] = fix[i]
key = "".join(key_list)
print("Ключ після виправлень:", key)
print(decrypt(cipher, key)[:200])
print("I розшифрованого:", round(calc_ic(decrypt(cipher, key)), 5))

# --- Дослідження впливу помилки у ключі ---
bad_key = "г" + key[1:]
bad_plain = decrypt(cipher, bad_key)

print("\nТекст з помилкою у ключі")
print("Ключ з помилкою:", bad_key)
for start in range(0, 160, r):
    print(bad_plain[start : start + r])
print("I розшифрованого:", round(calc_ic(bad_plain), 5))