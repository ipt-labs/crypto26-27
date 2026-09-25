ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
IDX = {c: i for i, c in enumerate(ALPHABET)}

def clean(text):
    text = text.lower().replace("ё", "е")
    return "".join(c for c in text if c in IDX)

def decrypt(text, key):
    r = len(key)
    return "".join(ALPHABET[(IDX[c] - IDX[key[i % r]]) % M] for i, c in enumerate(text))

with open("v3.txt", encoding="utf-8", errors="ignore") as f:
    y = clean(f.read())

key = "экомаятникфуко"   
pos = 0                  
new_letter = "а"         

good = decrypt(y, key)
bad_key = key[:pos] + new_letter + key[pos + 1:]
bad = decrypt(y, bad_key)

diff = [i for i in range(len(good)) if good[i] != bad[i]]

print("Правильний ключ: ", key)
print("Ключ з помилкою:", bad_key)
print("-" * 50)
print("Кількість зіпсованих літер:", len(diff), "із загальних", len(good))
print("Перші 10 позицій з помилками:", diff[:10])

distances = {diff[i+1] - diff[i] for i in range(min(50, len(diff)-1))}
print("Період між помилками:", distances)
print("-" * 50)
print("Текст правильний: ", good[:70])
print("Текст з помилкою:", bad[:70])