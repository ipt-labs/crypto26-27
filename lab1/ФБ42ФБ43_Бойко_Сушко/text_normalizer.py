import re

CLEAN_PATTERN = re.compile(r'[^а-яё]+')

def normalize_text(text: str) -> str:
    text = text.lower()
    
    text = CLEAN_PATTERN.sub(' ', text)
    
    return text.strip()

with open('Task3_natural.txt', 'r', encoding='utf-8') as f:
    text = f.read()

normalized = normalize_text(text)

with open('Task3_natural_normalized.txt', 'w', encoding='utf-8') as f:
    f.write(normalized)

with open('Task3_natural_normalized_no_spaces.txt', 'w', encoding='utf-8') as f:
    f.write(normalized.replace(' ', ''))