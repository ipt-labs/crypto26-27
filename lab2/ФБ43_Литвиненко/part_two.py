ru = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
bloks = list(range(1, 31))

# Зчитуємо шифротекст безпосередньо з файлу
with open(r"c:\Users\Tuf\Desktop\3 Курс\Крипта\lab2\variant9.txt", "r", encoding="utf-8") as f:
    text = f.read().lower()
print(f"Довжина шифротексту: {len(text)} символів\n")

def part2(text, r):
    ic_sum = 0
    for col in range(r):
        column_text = text[col::r]
        n = len(column_text)
        if n <= 1:
            continue
            
        frequencies = {}
        for char in column_text:
            frequencies[char] = frequencies.get(char, 0) + 1
            
        numerator = sum(count * (count - 1) for count in frequencies.values())
        denominator = n * (n - 1)
        ic_sum += numerator / denominator
        
    return ic_sum / r

for i in bloks:
    avg_ic = part2(text, i)
    print(f"Довжина ключа r = {i}: Середній IC = {avg_ic:.5f}")




#частина 3 ( знаходження ключа)

# 3. Відновлення ключа за допомогою частотного аналізу
m = len(ru)

russian_frequencies = {
    'о': 0.1098, 'е': 0.0848, 'а': 0.0799, 'н': 0.0670, 'т': 0.0631, 
    'и': 0.0630, 'с': 0.0547, 'р': 0.0473, 'в': 0.0454, 'л': 0.0434, 
    'к': 0.0348, 'м': 0.0321, 'д': 0.0298, 'п': 0.0281, 'у': 0.0262, 
    'я': 0.0201, 'ы': 0.0190, 'ь': 0.0174, 'г': 0.0169, 'з': 0.0165, 
    'б': 0.0159, 'ч': 0.0144, 'й': 0.0121, 'х': 0.0097, 'ж': 0.0094, 
    'ш': 0.0073, 'ю': 0.0065, 'ц': 0.0048, 'щ': 0.0036, 'э': 0.0032, 
    'ф': 0.0026, 'ъ': 0.0004
}

r = 17
recovered_key_chars = []

print("\n--- Відновлення ключа ---")
for col_idx in range(r):
    column_text = text[col_idx::r]
    best_shift = 0
    max_score = -1
    
    for shift in range(m):
        score = 0
        for char in column_text:
            if char in ru:
                char_idx = ru.index(char)
                orig_char = ru[(char_idx - shift) % m]
                score += russian_frequencies.get(orig_char, 0)
        
        if score > max_score:
            max_score = score
            best_shift = shift
            
    recovered_key_chars.append(ru[best_shift])

recovered_key = "".join(recovered_key_chars)
print(f"Знайдений ключ: {recovered_key}")

# 4. Розшифрування тексту
def decrypt_vigenere(cipher_text, key):
    decrypted = []
    key_len = len(key)
    for j, i in enumerate(cipher_text):
        if i in ru:
            y_id = ru.index(i)
            k_char = key[j % key_len]
            k_id = ru.index(k_char)
            x_id = (y_id - k_id + m) % m
            decrypted.append(ru[x_id])
        else:
            decrypted.append(i)
    return "".join(decrypted)

plain_text = decrypt_vigenere(text, recovered_key)

print("\n--- Розшифрований текст ---")
print(plain_text)



#4
# Створюємо зіпсований ключ (міняємо першу літеру 'в' на 'а')
bad_key_list = list(recovered_key)
bad_key_list[0] = 'а' # змінюємо першу літеру
bad_key = "".join(bad_key_list)

print(f"Правильний ключ:  {recovered_key}")
print(f"Зіпсований ключ: {bad_key}\n")

bad_plain_text = decrypt_vigenere(text, bad_key)

print("--- Розшифрований текст із помилкою в ключі (перші 300 символів) ---")
print(bad_plain_text[:300])