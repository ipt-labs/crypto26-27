import re

def preprocess_text(text: str, alphabet: str) -> tuple[str, str]:
    text = text.lower()
    alphabet = alphabet.lower()
    
    escaped_alphabet = re.escape(alphabet)
    pattern = f"[^{escaped_alphabet}]"
    text_with_spaces = re.sub(pattern, ' ', text)
    
    normalized_text = re.sub(r'\s+', ' ', text_with_spaces).strip()
    text_without_spaces = normalized_text.replace(' ', '')
    
    return normalized_text, text_without_spaces

if __name__ == "__main__":
    input_file = "Zavgorodnyaya_Tayna-treh-zerkal.txt"
    output_file_spaces = "output_with_spaces.txt"
    output_file_nospaces = "output_without_spaces.txt"
    russian_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text_from_file = f.read()
            
        lines_before = len(text_from_file.splitlines())
        chars_before = len(text_from_file)
        
        norm_text, no_space_text = preprocess_text(text_from_file, russian_alphabet)
        
        lines_after_norm = 1 if norm_text else 0
        chars_after_norm = len(norm_text)
        
        lines_after_nospace = 1 if no_space_text else 0
        chars_after_nospace = len(no_space_text)
        
        with open(output_file_spaces, 'w', encoding='utf-8') as f:
            f.write(norm_text + "\n")
            
        with open(output_file_nospaces, 'w', encoding='utf-8') as f:
            f.write(no_space_text + "\n")

        print(f"Кількість символів до нормалізації: {chars_before}")
        print(f"Кількість символів після нормалізації: {chars_after_norm}")
        print(f"Кількість символів після нормалізації та без пробілів: {chars_after_nospace}")
        
    except FileNotFoundError:
        print(f"Помилка: файл '{input_file}' не знайдено.")