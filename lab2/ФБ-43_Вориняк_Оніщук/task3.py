import collections
ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
M = len(ALPHABET)
CHAR_TO_INDEX = {char: idx for idx, char in enumerate(ALPHABET)}
INDEX_TO_CHAR = {idx: char for idx, char in enumerate(ALPHABET)}
P_T_DICT = {
    'о': 0.11370, 'е': 0.08903, 'а': 0.07880, 'и': 0.06670, 'н': 0.06560,
    'т': 0.06367, 'с': 0.05361, 'в': 0.05053, 'л': 0.04611, 'р': 0.04188,
    'м': 0.03203, 'к': 0.03114, 'д': 0.02973, 'п': 0.02820, 'у': 0.02770,
    'я': 0.02116, 'ь': 0.01955, 'ч': 0.01828, 'г': 0.01788, 'ы': 0.01740,
    'б': 0.01688, 'з': 0.01591, 'ж': 0.01084, 'й': 0.01024, 'ш': 0.00861,
    'х': 0.00797, 'ю': 0.00629, 'э': 0.00296, 'ц': 0.00290, 'щ': 0.00278,
    'ф': 0.00165, 'ъ': 0.00030
}
#Перетворюємо словник у список частот, де індекс списку відповідає індексу літери алфавіту
P_T = [P_T_DICT[char] for char in ALPHABET]

def crack_vigenere_key(ciphertext, r):
    # Розбиваємо шифртекст на r незалежних колонок
    blocks = [''] * r
    for i, char in enumerate(ciphertext):
        if char in CHAR_TO_INDEX:
            blocks[i % r] += char
    best_key = []
    print(f"{'Поз':<4} | {'Топ-1':<12} | {'Топ-2':<12} | {'Топ-3':<12}")
    print("-" * 47)
    
    for i, block in enumerate(blocks):
        block_len = len(block)
        counts = collections.Counter(block)
        #Обчислюємо фактичну відносну частоту кожної літери у поточному блоці
        block_freqs = [counts.get(char, 0) / block_len for char in ALPHABET]
        
        scores = []
        #Перебираємо всі можливі варіанти зсуву
        for g in range(M):
            #Якщо ключ g вірний, то літера c у шифртексті насправді є літерою (c-g)%M у відкритому тексті
            score = sum(block_freqs[c] * P_T[(c - g) % M] for c in range(M))
            scores.append((score, INDEX_TO_CHAR[g]))
        scores.sort(reverse=True, key=lambda x: x[0])
        best_key.append(scores[0][1])
        s1 = f"{scores[0][1]} ({scores[0][0]:.4f})"
        s2 = f"{scores[1][1]} ({scores[1][0]:.4f})"
        s3 = f"{scores[2][1]} ({scores[2][0]:.4f})"
        print(f"{i:2}   | {s1:<12} | {s2:<12} | {s3:<12}")
    return ''.join(best_key)

def decrypt_vigenere(text, key):
    r = len(key)
    plaintext = []
    #x_i = (y_i - k_i) mod M
    for i, char in enumerate(text):
        if char in CHAR_TO_INDEX:
            y_i = CHAR_TO_INDEX[char]
            k_i = CHAR_TO_INDEX[key[i % r]]
            x_i = (y_i - k_i) % M
            plaintext.append(INDEX_TO_CHAR[x_i])        
    res = ''.join(plaintext)
    with open('variant8_decrypted.txt', 'w', encoding='utf-8') as f:
        f.write(res)
    return res

if __name__ == "__main__":
    with open('variant8.txt', 'r', encoding='utf-8') as f:
        ciphertext = f.read().strip()
    found_key = crack_vigenere_key(ciphertext, 20)
    print(f"\n[+] Найімовірніший ключ: {found_key}")

    decrypt_vigenere(ciphertext, found_key)
    print("[+] Відкритий текст збережено у 'variant8_decrypted.txt'")