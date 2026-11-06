import re
text = open("garri_potter_i_orden_feniksa.u.txt", encoding="utf-8").read().lower().replace("ё", "е")
text = re.sub("[^а-я]+", " ", text).strip()
text_without_spaces = text.replace(" ", "")
open("garri_potter_i_orden_feniksa.u_готово.txt", "w", encoding="utf-8").write(text)
print("Готово")
