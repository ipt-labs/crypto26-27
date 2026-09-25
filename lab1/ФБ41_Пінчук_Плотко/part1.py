import re
import sys
from pathlib import Path

# Алфавіт: 32 літери (ё -> е), ъ та ь окремо. Пробіл - окремий символ.
LETTERS = "абвгдежзийклмнопрстуфхцчшщъыьэюя"


def clean(text: str, keep_spaces: bool = True) -> str:
    text = text.lower()                          # усі літери в нижній регістр
    text = text.replace("ё", "е")                # ё -> е
    text = re.sub(f"[^{LETTERS}]+", " ", text)   # не-літери -> пробіл,
                                                 # послідовність символів -> один пробіл
    text = text.strip()
    if not keep_spaces:
        text = text.replace(" ", "")             # версія без пробілів
    return text


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Використання: python step1_prepare.py <файл_UTF-8>")

    raw = Path(sys.argv[1]).read_text(encoding="utf-8")

    with_spaces = clean(raw, keep_spaces=True)
    no_spaces = clean(raw, keep_spaces=False)

    Path("text_with_spaces.txt").write_text(with_spaces, encoding="utf-8")
    Path("text_no_spaces.txt").write_text(no_spaces, encoding="utf-8")

    print(f"вихідний текст:  {len(raw)} символів")
    print(f"з пробілами:     {len(with_spaces)} символів, "
          f"різних символів: {len(set(with_spaces))}")
    print(f"без пробілів:    {len(no_spaces)} символів, "
          f"різних символів: {len(set(no_spaces))}")


if __name__ == "__main__":
    main()