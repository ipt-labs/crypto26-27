import re

text = open("besy.txt", encoding="utf-8").read().lower()
text = text.replace("ё", "е").replace(chr(0x301), "")
text = re.sub("[^абвгдежзийклмнопрстуфхцчшщъыьэюя]+", " ", text).strip()

open("text_spaces.txt", "w", encoding="utf-8").write(text)
open("text_nospaces.txt", "w", encoding="utf-8").write(text.replace(" ", ""))

print("з пробілами:", len(text))
print("без пробілів:", len(text.replace(" ", "")))
print("символів в алфавіті:", len(set(text)))
