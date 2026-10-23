from task1 import ALPHABET, coincidence_index, load_text

def main():
    text = load_text("variant6.txt")
    n = len(text)
    print(f"{'r':>3} {'mean I':>10} {'D_r share':>10}")
    for r in range(2, 36):
        blocks = [text[i::r] for i in range(r)]
        mean_i = sum(coincidence_index(b) for b in blocks) / r
        matches = sum(1 for i in range(n - r) if text[i] == text[i + r])
        print(f"{r:3d} {mean_i:10.6f} {matches / (n - r):10.5f}")

if __name__ == "__main__":
    main()