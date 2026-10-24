from pathlib import Path

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
FOLDER = Path(__file__).resolve().parent
KEY = "делолисоборотней"


def decrypt(text, key):
    result = ""
    for i, char in enumerate(text):
        y = ALPHABET.index(char)
        k = ALPHABET.index(key[i % len(key)])
        result += ALPHABET[(y - k) % 32]
    return result


if __name__ == "__main__":
    input_file1 = "variant5.txt"
    with open(input_file1, 'r', encoding='utf-8') as f:
       ciphertext= f.read()
    wrong_key = "е" + KEY[1:]
    expected_count = (len(ciphertext) - 1) // len(KEY) + 1
    print("Правильний ключ:", KEY)
    print("Помилковий ключ:", wrong_key)
    print(f"Прогноз: зміняться позиції 1, 17, 33, ...; разом {expected_count}.")
    print("Літери зсунуться на -1 за модулем 32; інші не зміняться.")
    print()

    correct = decrypt(ciphertext, KEY)
    wrong = decrypt(ciphertext, wrong_key)
    positions = [i + 1 for i in range(len(correct)) if correct[i] != wrong[i]]
    expected_positions = list(range(1, len(ciphertext) + 1, len(KEY)))
    shifts = {(ALPHABET.index(wrong[i - 1]) - ALPHABET.index(correct[i - 1])) % 32
              for i in positions}
    print(f"Змінено {len(positions)} з {len(ciphertext)} літер ({100 * len(positions) / len(ciphertext):.4f} %)")
    print("Перші змінені позиції:", ", ".join(str(i) for i in positions[:8]))
    print("Позиції збігаються з прогнозом:", positions == expected_positions)
    print("Усі зсуви дорівнюють -1 mod 32:", shifts == {31})
    print()
    print("Правильний текст:")
    print(correct[:76])
    print("Текст із помилкою:")
    print(wrong[:76])
