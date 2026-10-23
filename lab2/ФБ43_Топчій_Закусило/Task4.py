from Task1 import ALPHABET, M, encrypt, load_text

R = 17
KEY = "возвращениеджинна"
POSITION = 5
NEW_LETTER = "ф"


def decrypt(text, key):
    inverse = "".join(ALPHABET[(-ALPHABET.index(c)) % M] for c in key)
    return encrypt(text, inverse)


def main():
    text = load_text("variant6.txt")

    wrong_key = KEY[:POSITION] + NEW_LETTER + KEY[POSITION + 1:]
    print(f"original key: {KEY}")
    print(f"modified key: {wrong_key}")

    delta = (ALPHABET.index(NEW_LETTER) - ALPHABET.index(KEY[POSITION])) % M
    print(f"delta = {delta} ({ALPHABET[delta]})")

    plain = decrypt(text, KEY)
    broken = decrypt(text, wrong_key)

    errors = [i for i in range(len(text)) if plain[i] != broken[i]]
    print(f"total mismatches: {len(errors)}")
    print(f"error positions mod 17: {sorted(set(i % R for i in errors))}")

    for i in errors[:15]:
        print(f"pos {i}: {plain[i]} become {broken[i]}")

    print(f"head with wrong key: {broken[:120]}")


if __name__ == "__main__":
    main()