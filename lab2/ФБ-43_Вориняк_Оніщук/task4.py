ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
M = len(ALPHABET)
CHAR_TO_INDEX = {char: idx for idx, char in enumerate(ALPHABET)}
INDEX_TO_CHAR = {idx: char for idx, char in enumerate(ALPHABET)}

def decrypt_vigenere(text, key):
    r = len(key)
    plaintext = []
    for i, char in enumerate(text):
        if char in CHAR_TO_INDEX:
            y_i = CHAR_TO_INDEX[char]
            k_i = CHAR_TO_INDEX[key[i % r]]
            x_i = (y_i - k_i) % M
            plaintext.append(INDEX_TO_CHAR[x_i])
    return ''.join(plaintext)

if __name__ == "__main__":
    with open('variant8.txt', 'r', encoding='utf-8') as f:
        ciphertext = f.read().strip()
    correct_key = "улановсеребряныепули"
    wrong_key = "алановсеребряныепули" 
    
    correct_text = decrypt_vigenere(ciphertext, correct_key)
    wrong_text = decrypt_vigenere(ciphertext, wrong_key)
    with open('variant8_error.txt', 'w', encoding='utf-8') as f:
        f.write(wrong_text)
        
    print(f"Ключ: {correct_key}")
    print(f"[+] Текст: {correct_text[:60]}")
    print("-" * 71)
    print(f"Ключ: {wrong_key}")
    print(f"[+] Текст: {wrong_text[:60]}")