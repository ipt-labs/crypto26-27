import re

input = "text.txt"

normalized = "normalized.txt"
no_spaces = "withoutSpaces.txt"

alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def normalize_text(text):
    text = text.lower()
    text = re.sub(f"[^{alphabet}\\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


with open(input, "r", encoding="utf-8") as file:
    text = file.read()

normalized_text = normalize_text(text)
text_without_spaces = normalized_text.replace(" ", "")

with open(normalized, "w", encoding="utf-8") as file:
    file.write(normalized_text)

with open(no_spaces, "w", encoding="utf-8") as file:
    file.write(text_without_spaces)
