import random

alphabet_pattern = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
sequence_d = alphabet_pattern * 10000

sequence_g_list = list(sequence_d)

random.shuffle(sequence_g_list)

sequence_g = "".join(sequence_g_list)

with open('Task4_periodic.txt', 'w', encoding='utf-8') as f:
    f.write(sequence_d)

with open('Task4_random.txt', 'w', encoding='utf-8') as f:
    f.write(sequence_g)

