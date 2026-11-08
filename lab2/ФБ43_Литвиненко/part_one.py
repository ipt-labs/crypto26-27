ru = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
m = len(ru)
kys = ['да', 'том', 'перо', 'весна', 'криптоанализатор']

def prepare_text():
    with open(r"c:\Users\Tuf\Desktop\3 Курс\Крипта\lab2\text.txt", "r", encoding="utf-8") as f:
        x = f.read().lower()
    cleaned = []
    for i in x:
        if i == 'ё':
            i = 'е'
        if i in ru:
            cleaned.append(i)
    return "".join(cleaned)

def vigenere(text, key):
    encrypted = []
    key_len = len(key)
    
    for j, i in enumerate(text):
        x_id = ru.index(i)        
        k_char = key[j % key_len]    
        k_id = ru.index(k_char)    

        y_id = (x_id + k_id) % m
        encrypted.append(ru[y_id])
    return "".join(encrypted)


# Функція для розрахунку індексу відповідності
def index_of_coincidence(text):
    n = len(text)
    if n <= 1:
        return 0.0
    
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1
        
    # Формула 
    numerator = sum(count * (count - 1) for count in frequencies.values())
    denominator = n * (n - 1)
    
    return numerator / denominator


clean_text = prepare_text()
print(f"Довжина тексту: {len(clean_text)} символів\n")

ic_open = index_of_coincidence(clean_text)
print(f"Відкритий текст: Індекс відповідності I = {ic_open:.5f}")
print("-" * 50)

# 2. Шифруємо і рахуємо індекси для кожного ключа
for k in kys:
    shifr_text = vigenere(clean_text, k)
    ic_cipher = index_of_coincidence(shifr_text)
    print(f"Ключ: '{k}' (r={len(k)}): Індекс відповідності I = {ic_cipher:.5f}")
    print("\n")
    print(f"Зашифрований текст ключем {k}: {shifr_text} \n")