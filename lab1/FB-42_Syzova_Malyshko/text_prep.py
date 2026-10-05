import re
import os

def preprocess_text(input_file, output_spaces, output_nospaces):
    print(f"Починаємо обробку файлу: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read().lower()
    except UnicodeDecodeError:
        with open(input_file, 'r', encoding='cp1251') as f:
            text = f.read().lower()

    text = re.sub(r'[^а-яё\s]', ' ', text)  
    text_with_spaces = re.sub(r'\s+', ' ', text).strip()
    text_no_spaces = text_with_spaces.replace(' ', '')

    with open(output_spaces, 'w', encoding='utf-8') as f1:
        f1.write(text_with_spaces)
        
    with open(output_nospaces, 'w', encoding='utf-8') as f2:
        f2.write(text_no_spaces)

    print("Обробку завершено успішно!")
    print(f"Довжина тексту з пробілами: {len(text_with_spaces)} символів")
    print(f"Довжина тексту без пробілів: {len(text_no_spaces)} символів")

if __name__ == "__main__":
    preprocess_text('raw_text.txt', 'text_spaces.txt', 'text_nospaces.txt')