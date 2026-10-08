import os
import collections

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
CHAR_TO_IDX = {ch: i for i, ch in enumerate(ALPHABET)}
IDX_TO_CHAR = {i: ch for i, ch in enumerate(ALPHABET)}

RUS_FREQS = {
    'о': 0.1097, 'е': 0.0845, 'а': 0.0801, 'и': 0.0735, 'н': 0.0670,
    'т': 0.0626, 'с': 0.0547, 'р': 0.0473, 'в': 0.0454, 'л': 0.0440,
    'к': 0.0349, 'м': 0.0320, 'д': 0.0298, 'п': 0.0281, 'у': 0.0262,
    'я': 0.0201, 'ы': 0.0190, 'ь': 0.0174, 'г': 0.0170, 'з': 0.0165,
    'б': 0.0159, 'ч': 0.0144, 'й': 0.0121, 'х': 0.0097, 'ж': 0.0094,
    'ш': 0.0073, 'ю': 0.0064, 'ц': 0.0048, 'щ': 0.0036, 'э': 0.0032,
    'ф': 0.0026, 'ъ': 0.0004
}

def index_of_coincidence(text):
    n = len(text)
    if n <= 1:
        return 0.0
    counts = collections.Counter(text)
    return sum(cnt * (cnt - 1) for cnt in counts.values()) / (n * (n - 1))

def coincidence_count(text, r):
    return sum(1 for i in range(len(text) - r) if text[i] == text[i + r])

def analyze_period(ciphertext, max_r=30):
    results = []
    for r in range(2, max_r + 1):
        blocks = [ciphertext[i::r] for i in range(r)]
        avg_ic = sum(index_of_coincidence(b) for b in blocks) / r
        d_r = coincidence_count(ciphertext, r)
        results.append((r, avg_ic, d_r))
    return results

def find_key(ciphertext, r):
    key = []
    for j in range(r):
        block = ciphertext[j::r]
        n_block = len(block)
        counts = collections.Counter(block)
        best_g = 0
        max_corr = -1.0
        for g in range(M):
            corr = 0.0
            for ch, p_t in RUS_FREQS.items():
                t = CHAR_TO_IDX[ch]
                shifted_char = IDX_TO_CHAR[(t + g) % M]
                corr += p_t * (counts.get(shifted_char, 0) / n_block)
            if corr > max_corr:
                max_corr = corr
                best_g = g
        key.append(IDX_TO_CHAR[best_g])
    return "".join(key)

def decrypt(ciphertext, key):
    r = len(key)
    plaintext = []
    for i, ch in enumerate(ciphertext):
        c_val = CHAR_TO_IDX[ch]
        k_val = CHAR_TO_IDX[key[i % r]]
        p_val = (c_val - k_val) % M
        plaintext.append(IDX_TO_CHAR[p_val])
    return "".join(plaintext)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "variant_1.txt")

    if not os.path.exists(file_path):
        print(f"Помилка: файл '{file_path}' не знайдено!")
        exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read()

    ciphertext = "".join([c.lower() for c in raw if c.lower() in ALPHABET])

    print(f"Довжина шифртексту: {len(ciphertext)} символів\n")

    stats = analyze_period(ciphertext, max_r=30)
    
    best_r = None
    for r, ic, dr in stats:
        if ic > 0.048:
            best_r = r
            break
    if not best_r:
        best_r = max(stats, key=lambda x: x[1])[0]

    print(f"{'r':<4} | {'Avg IC':<10} | {'D_r':<6}")
    print("-" * 25)
    for r, ic, dr in stats:
        flag = " <--- ІСТИННИЙ ПЕРІОД!" if r == best_r else (" <--- КРАТНИЙ!" if r % best_r == 0 else "")
        print(f"{r:<4} | {ic:<10.5f} | {dr:<6}{flag}")

    key = find_key(ciphertext, best_r)
    print(f"\n[+] Знайдена довжина ключа: r = {best_r}")
    print(f"[+] Відновлений ключ: {key}")

    decrypted_text = decrypt(ciphertext, key)
    print(f"\n[+] Розшифрований текст (перші 350 символів):")
    print(decrypted_text[:350] + "...")

    bad_key = ("б" if key[0] != "б" else "а") + key[1:]
    bad_decrypted_text = decrypt(ciphertext, bad_key)
    print(f"\n[+] Текст зі зміненим символом ключа ('{bad_key}'):")
    print(bad_decrypted_text[:140] + "...")