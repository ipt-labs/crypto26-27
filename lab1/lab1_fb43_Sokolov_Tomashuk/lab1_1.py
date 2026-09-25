import re


def preprocess_text(input_filepath):
    try:
        with open(input_filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()
    except UnicodeDecodeError:
        with open(input_filepath, "r", encoding="cp1251") as f:
            raw_text = f.read()

    text = raw_text.lower()

    text = text.replace("ё", "е")

    text_with_spaces = re.sub(r"[^а-я\s]", " ", text)
    text_with_spaces = re.sub(r"\s+", " ", text_with_spaces).strip()

    text_without_spaces = text_with_spaces.replace(" ", "")

    with open("text_with_spaces.txt", "w", encoding="utf-8") as f:
        f.write(text_with_spaces)

    with open("text_without_spaces.txt", "w", encoding="utf-8") as f:
        f.write(text_without_spaces)

    print("Попередня обробка завершена успішно!")
    print(f"Кількість символів (з пробілами): {len(text_with_spaces)}")
    print(f"Кількість символів (без пробілів): {len(text_without_spaces)}")


preprocess_text("Тихий Дон. Михаил Шолохов.txt")