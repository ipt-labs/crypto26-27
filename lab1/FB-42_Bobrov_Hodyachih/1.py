import os
import re

DIR = os.path.dirname(os.path.abspath(__file__))
inputf = os.path.join(DIR, "war_peace.txt")
output = os.path.join(DIR, "cleaned_war.txt")
output_nospace = os.path.join(DIR, "cleaned_war_nospaces.txt")

with open(inputf, "r", encoding="utf-8") as f:
    text = f.read()

text = text.lower()
text = text.replace("ё", "е")
text = re.sub(r"[^а-я\s]", " ", text)
text = re.sub(r"\s+", " ", text).strip()
print(f"Довжина тексту з пробілами: {len(text)} символів")
with open(output, "w", encoding="utf-8") as f:
    f.write(text)

text_nospaces = text.replace(" ", "")
print(f"Довжина тексту без пробілів: {len(text_nospaces)} символів")
with open(output_nospace, "w", encoding="utf-8") as f:
    f.write(text_nospaces)