import math
from collections import Counter
import os

def calculate_entropy(frequencies, total_count, n_gram_length=1):
    """Обчислює ентропію на символ за заданими частотами."""
    entropy = 0
    for count in frequencies.values():
        probability = count / total_count
        entropy -= probability * math.log2(probability)
    
    return entropy / n_gram_length

def analyze_text(filename, n_gram_type='unigram', step=1):
    """Аналізує текст і повертає частоти та ентропію."""
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    text_length = len(text)
    
    if n_gram_type == 'unigram':
        frequencies = Counter(text)
        total_count = text_length
        entropy = calculate_entropy(frequencies, total_count, 1)
        
    elif n_gram_type == 'bigram':
        
        bigrams = [text[i:i+2] for i in range(0, text_length - 1, step)]
        
        if step == 2 and len(bigrams[-1]) == 1:
            bigrams = bigrams[:-1]
            
        frequencies = Counter(bigrams)
        total_count = len(bigrams)
        entropy = calculate_entropy(frequencies, total_count, 2)
        
    top_5 = dict(frequencies.most_common(5))
    return top_5, entropy

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_spaces = os.path.join(script_dir, 'text_spaces.txt')
    file_nospaces = os.path.join(script_dir, 'text_nospaces.txt')
    
    print("ТЕКСТ З ПРОБІЛАМИ ")
    top_sym_sp, h1_sp = analyze_text(file_spaces, 'unigram')
    print(f"H1: {h1_sp:.5f}")
    print(f"Топ-5 символів: {top_sym_sp}")
    
    top_bi_sp_cross, h2_sp_cross = analyze_text(file_spaces, 'bigram', step=1)
    print(f"H2 (перетинаються): {h2_sp_cross:.5f}")
    print(f"Топ-5 біграм: {top_bi_sp_cross}")
    
    top_bi_sp_nocross, h2_sp_nocross = analyze_text(file_spaces, 'bigram', step=2)
    print(f"H2 (не перетинаються): {h2_sp_nocross:.5f}")
    print(f"Топ-5 біграм: {top_bi_sp_nocross}\n")
    
    print("ТЕКСТ БЕЗ ПРОБІЛІВ")
    top_sym_nosp, h1_nosp = analyze_text(file_nospaces, 'unigram')
    print(f"H1: {h1_nosp:.5f}")
    print(f"Топ-5 символів: {top_sym_nosp}")
    
    top_bi_nosp_cross, h2_nosp_cross = analyze_text(file_nospaces, 'bigram', step=1)
    print(f"H2 (перетинаються): {h2_nosp_cross:.5f}")
    print(f"Топ-5 біграм: {top_bi_nosp_cross}")
    
    top_bi_nosp_nocross, h2_nosp_nocross = analyze_text(file_nospaces, 'bigram', step=2)
    print(f"H2 (не перетинаються): {h2_nosp_nocross:.5f}")
    print(f"Топ-5 біграм: {top_bi_nosp_nocross}")