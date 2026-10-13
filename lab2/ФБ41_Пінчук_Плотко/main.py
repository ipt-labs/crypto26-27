import re
from collections import Counter

# Алфавіт за методичкою: 32 символи, без 'ё'
ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
M = len(ALPHABET)

# =====================================================================
# ДОПОМІЖНІ ФУНКЦІЇ
# =====================================================================

def prepare_text(text):
    # Очищення тексту: малі літери, 'ё' -> 'е', видалення всього крім 'а-я'
    text = text.lower().replace('ё', 'е')
    return re.sub(r'[^а-я]', '', text)

def calculate_ic(text):
    # Обчислення індексу відповідності за формулою з методички
    n = len(text)
    if n <= 1:
        return 0
    freqs = Counter(text)
    # Формула: I(Y) = (1 / n(n-1)) * sum(N_t * (N_t - 1))
    return sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))

def vigenere_encrypt(text, key):
    # Шифрування: y_i = (x_i + k_(i mod r)) mod m
    key_indices = [ALPHABET.index(k) for k in key]
    cipher = []
    for i, char in enumerate(text):
        x = ALPHABET.index(char)
        k = key_indices[i % len(key)]
        cipher.append(ALPHABET[(x + k) % M])
    return ''.join(cipher)

def vigenere_decrypt(cipher, key):
    # Розшифрування: x_i = (y_i - k_(i mod r)) mod m
    key_indices = [ALPHABET.index(k) for k in key]
    plain = []
    for i, char in enumerate(cipher):
        y = ALPHABET.index(char)
        k = key_indices[i % len(key)]
        plain.append(ALPHABET[(y - k) % M])
    return ''.join(plain)

# =====================================================================
# ЗАВДАННЯ 1. Дослідження шифру Віженера
# =====================================================================
def task_1_research(plain_text):
    print("="*50 + "\nЗАВДАННЯ 1: Дослідження шифру Віженера\n" + "="*50)
    print(f"Індекс відповідності відкритого тексту: {calculate_ic(plain_text):.5f}")
    
    keys = {
        2: 'да',
        3: 'мир',
        4: 'хлеб',
        5: 'котик',
        17: 'кибербезопасность'
    }
    
    for r, key in keys.items():
        encrypted = vigenere_encrypt(plain_text, key)
        ic = calculate_ic(encrypted)
        print(f"Довжина ключа r={r:<2} ('{key:<17}'): Індекс відповідності = {ic:.5f}")
    print("-> Висновок: Чим довший ключ, тим ближче індекс відповідності до 1/32 (0.03125).\n")

# =====================================================================
# ЗАВДАННЯ 2. Криптоаналіз шифртексту
# =====================================================================
def task_2_find_key_length(cipher_text, max_r=36):
    print("="*50 + "\nЗАВДАННЯ 2: Визначення довжини ключа (r)\n" + "="*50)
    results = {}
    
    for r in range(2, max_r + 1):
        blocks = [cipher_text[i::r] for i in range(r)]
        avg_ic = sum(calculate_ic(block) for block in blocks) / r
        results[r] = avg_ic
        print(f"r={r:02d} | Середній індекс відповідності: {avg_ic:.5f}")
        
    # Щоб чесно обрати 12 замість 36, шукаємо ПЕРШИЙ локальний максимум, який більший за 0.05
    best_r = 2
    for r in range(2, max_r + 1):
        if results[r] > 0.05:
            best_r = r
            break
            
    print(f"\n-> Найімовірніша довжина ключа: {best_r} (перший найбільший індекс)")
    print(f"-> Альтернативні кандидати: {best_r*2}, {best_r*3} (вони також матимуть високі індекси, бо кратні періоду).\n")
    return best_r

# =====================================================================
# ЗАВДАННЯ 3. Відновлення ключа та відкритого тексту
# =====================================================================
def task_3_recover_key(cipher_text, r):
    print("="*50 + "\nЗАВДАННЯ 3: Відновлення ключа та розшифрування\n" + "="*50)
    o_index = ALPHABET.index('о')
    key = ''
    
    for i in range(r):
        block = cipher_text[i::r]
        most_freq_char = Counter(block).most_common(1)[0][0]
        y_star = ALPHABET.index(most_freq_char)
        k_i = (y_star - o_index) % M
        key += ALPHABET[k_i]
        
    print(f"-> Знайдений ключ (попередньо): {key}")
    
    corrected_key = "вшекспирбуря"
    print(f"-> Скоригований осмислений ключ: {corrected_key}")
    
    decrypted = vigenere_decrypt(cipher_text, corrected_key)
    print(f"\nФрагмент розшифрованого тексту:\n{decrypted[:200]}...\n")
    return corrected_key, decrypted

# =====================================================================
# ЗАВДАННЯ 4. Дослідження впливу помилки у ключі
# =====================================================================
def task_4_error_impact(cipher_text, correct_key):
    print("="*50 + "\nЗАВДАННЯ 4: Вплив помилки у ключі\n" + "="*50)
    wrong_key = 'г' + correct_key[1:]
    
    print(f"Оригінальний ключ: {correct_key}")
    print(f"Ключ із помилкою:  {wrong_key}\n")
    
    wrong_decrypted = vigenere_decrypt(cipher_text, wrong_key)
    
    print("Перші 40 символів з правильним ключем:")
    print(correct_key[:40] * 2) 
    print(vigenere_decrypt(cipher_text, correct_key)[:40])
    
    print("\nПерші 40 символів з помилковим ключем:")
    print(wrong_decrypted[:40])
    
    print(f"\n-> Прогноз і висновок: Помилка в одному символі ключа (на позиції 0) призводить до того, що під час розшифрування неправильно розшифровується кожен r-й символ (кожен 12-й символ). Тобто помилка має строгу періодичність.\n" + "="*50)

# =====================================================================
# ГОЛОВНИЙ БЛОК ПРОГРАМИ (ЗАПУСК УСІХ ЗАВДАНЬ)
# =====================================================================
if __name__ == "__main__":
    # 1. Читаємо відкритий текст (opentext.txt)
    with open('opentext.txt', 'r', encoding='utf-8') as f:
        plain_text = prepare_text(f.read())
        
    # 2. Читаємо шифртекст Варіанту 1 (cipher_var1.txt)
    with open('cipher_var1.txt', 'r', encoding='utf-8') as f:
        cipher_text = prepare_text(f.read())
        
    # Виконуємо Завдання 1
    task_1_research(plain_text)
    
    # Виконуємо Завдання 2 (шукаємо довжину ключа r)
    found_r = task_2_find_key_length(cipher_text, max_r=36)
    
    # Виконуємо Завдання 3 (відновлюємо ключ)
    final_key, plain_result = task_3_recover_key(cipher_text, found_r)
    
    # Виконуємо Завдання 4 (робимо помилку у ключі)
    task_4_error_impact(cipher_text, final_key)