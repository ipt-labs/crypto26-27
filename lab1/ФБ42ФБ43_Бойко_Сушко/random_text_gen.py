import random

ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

def generate_max_entropy_text(length):
    return "".join(random.choices(ALPHABET, k=length))

random_text = generate_max_entropy_text(34279)

with open('Task3_random_no_spaces.txt', 'w', encoding='utf-8') as f:
    f.write(random_text)
