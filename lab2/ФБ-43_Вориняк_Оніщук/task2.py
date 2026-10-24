import collections
ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

def calculate_ic(text):
    n = len(text)
    if n <= 1:
        return 0
    counts = collections.Counter(text)
    return sum(c * (c-1) for c in counts.values()) / (n*(n-1))

def find_key_length(ciphertext, max_len=30):
    #Знаходимо ймовірну довжину ключа методом усереднення індексу відповідності
    results = []
    for r in range(2, max_len + 1):
        blocks = [''] * r
        for i, char in enumerate(ciphertext):
            blocks[i % r] += char
        ic_sum = sum(calculate_ic(block) for block in blocks)
        avg_ic = ic_sum / r
        results.append((r, avg_ic))
    return results

if __name__ == "__main__":
    try:
        with open('variant8.txt', 'r', encoding='utf-8') as f:
            ciphertext = f.read().strip()
    except FileNotFoundError:
        print("Файл 'variant8.txt' не знайдено.")
        exit()
    ic_results = find_key_length(ciphertext)
    
    print(" r | Середній Ic")
    print("=" * 16)
    for r, avg_ic in ic_results:
        marker = "< Ймовірний період (або кратне)" if avg_ic > 0.050 else ""
        print(f"{r:2} | {avg_ic:.5f} {marker}")