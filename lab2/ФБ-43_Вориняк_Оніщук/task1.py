import collections

ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
M = len(ALPHABET)
CHAR_TO_INDEX = {char: idx for idx, char in enumerate(ALPHABET)}
INDEX_TO_CHAR = {idx: char for idx, char in enumerate(ALPHABET)}

def calculate_ic(text):
    n = len(text)
    if n <= 1:
        return 0
    counts = collections.Counter(text)
    # N_t*(N_t-1) / n*(n - 1)
    ic = sum(count * (count - 1) for count in counts.values()) / (n * (n - 1))
    return ic

def encrypt_vigenere(text, key, output_filename):
    r = len(key)
    ciphertext = []
    
    for i, char in enumerate(text):
        if char in CHAR_TO_INDEX:
            x_i = CHAR_TO_INDEX[char]
            k_i = CHAR_TO_INDEX[key[i % r]]            
            y_i = (x_i + k_i) % M
            ciphertext.append(INDEX_TO_CHAR[y_i])
    result_text = ''.join(ciphertext)
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(result_text)    
    print(f"  Ключ: '{key}' (r={r}). Результат збережено у {output_filename}")
    return result_text

if __name__ == "__main__":
    print(f"Теоретичний Ic відкритого тексту: 0.05637")
    print(f"Теоретичний Ic рівноймовірного алфавіту: 0.03125")
    try:
        with open('open_text_panteleriya.txt', 'r', encoding='utf-8') as f:
            open_text = f.read().strip()
    except FileNotFoundError:
        print("[!] Файл 'open_text_panteleriya.txt' не знайдено.")
        exit()
    ic_open = calculate_ic(open_text)
    print(f"\nIc відкритого тексту ({len(open_text)} символів): {ic_open:.5f}")

    keys = ["ок", "чак", "небо", "весна", "делорианзабылинавек"]    
    for key in keys:
        out_file = f"panteleriya_r{len(key)}.txt"
        cipher = encrypt_vigenere(open_text, key, out_file)
        ic_cipher = calculate_ic(cipher)
        print(f"  > Ic шифртексту: {ic_cipher:.5f}\n")