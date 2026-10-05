import math
import random
from collections import Counter
import os

def calc_h1(text):
    frequencies = Counter(text)
    entropy = 0
    total = len(text)
    for count in frequencies.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_spaces = os.path.join(script_dir, 'text_spaces.txt')
    
    with open(file_spaces, 'r', encoding='utf-8') as f:
        seq_A = f.read()[:10000]   
   
    seq_B = 'а' * 10000
    
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
    seq_C = ''.join(random.choices(alphabet, k=10000))
    
    print(f"H1 (Б - один символ): {calc_h1(seq_B):.5f}")
    print(f"H1 (А - природний текст): {calc_h1(seq_A):.5f}")
    print(f"H1 (В - випадкова): {calc_h1(seq_C):.5f}")