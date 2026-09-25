import re

INPUT_PATH = "brothers_karamazov.txt"
OUTPUT_WITH_SPACES = "brothers_karamazov_clean_with_spaces.txt"
OUTPUT_NO_SPACES = "brothers_karamazov_clean_no_spaces.txt"

def preprocess_text(input_file: str):
    with open(input_file, "r", encoding="windows-1251") as f:
        text = f.read()

    text_lower = text.lower()
    text_cleaned = re.sub(r"[^а-яё]", " ", text_lower)
    text_with_spaces = re.sub(r"\s+", " ", text_cleaned).strip()
    text_no_spaces = text_with_spaces.replace(" ", "")

    with open(OUTPUT_WITH_SPACES, "w", encoding="utf-8") as f:
        f.write(text_with_spaces)
    with open(OUTPUT_NO_SPACES, "w", encoding="utf-8") as f:
        f.write(text_no_spaces)

    print("Попередня обробка завершена:")
    print(f" - З пробілами: {len(text_with_spaces):,} символів -> {OUTPUT_WITH_SPACES}")
    print(f" - Без пробілів: {len(text_no_spaces):,} символів -> {OUTPUT_NO_SPACES}")

if __name__ == "__main__":
    preprocess_text(INPUT_PATH)