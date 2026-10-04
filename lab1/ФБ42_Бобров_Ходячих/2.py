from collections import Counter
import math
import os

def calc_stats(text, n, step):
    ngrams = [text[i : i + n] for i in range(0, len(text) - n + 1, step)]
    counts = Counter(ngrams) 
    total = len(ngrams)
    freqs = {k: v / total for k, v in counts.items()} # частота n-грам
    h = -sum(p * math.log2(p) for p in freqs.values() if p > 0) / n # Питома ентропія
    return counts, freqs, h

def analyse(file_path, description):
    print("=" * 50)
    print(f" РЕЗУЛЬТАТИ ДЛЯ: {description}")
    print("=" * 50)

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"Довжина тексту: {len(text)} символів\n")

    modes = [
        ("Монограми (H1)", "H1", 1, 1, "символів"),
        ("Біграми, що перетинаються (H2)","H2 (перетинаються)",2,1,"біграм",),
        ("Біграми, що не перетинаються (H2)","H2 (не перетинаються)",2,2,"біграм",),
        #("10Біграми, що не перетинаються (H2)","H2 (не перетинаються)",10,1,"біграм",),
    ]

    for title, h_label, n, step, item_label in modes:
        counts, freqs, h_val = calc_stats(text, n=n, step=step)
        sorted_items = sorted(freqs.items(), key=lambda x: x[1], reverse=True)[:32]
        top5 = [(item, freq, counts[item]) for item, freq in sorted_items]
        #print(len(counts))

        print(f"--- {title} ---")
        print(f"{h_label} = {h_val:.6f} біт/символ")
        print(f"Топ-5 найчастіших {item_label}:")
        for item, freq, count in top5:
            print(f"{repr(item)}: {freq:.6f} ({count})")
        print()

DIR = os.path.dirname(os.path.abspath(__file__))
analyse(os.path.join(DIR, "cleaned_war.txt"), "cleaned_war.txt")
analyse(os.path.join(DIR, "cleaned_war_nospaces.txt"), "cleaned_war_nospaces.txt")