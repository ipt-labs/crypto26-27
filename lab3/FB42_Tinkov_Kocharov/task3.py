from itertools import permutations
from common import (
    ALPHABETS, FREQ_LETTERS, LANG_BIGRAMS, M, M2, RARE_LETTERS, bigram_to_num,
    clean, decrypt, letter_freq, read, solve_congruence,
)
from lab1_common import bigram_freqs

CIPHER = '07.txt'
TEST = 'V7.txt'
REFERENCE = 'bratia_karamazovy.txt'
FREQ_MIN = 0.20
RARE_MAX = 0.05

ref = clean(read(REFERENCE, 'cp1251'))
rf = letter_freq(ref, ALPHABETS[0])
print('РОЗПІЗНАВАЧ РОСІЙСЬКОЇ МОВИ')
print(f'  часті {"+".join(FREQ_LETTERS)}: еталон '
      f'{sum(rf[c] for c in FREQ_LETTERS):.4f}, випадковий текст {3 / M:.4f}, '
      f'поріг > {FREQ_MIN}')
print(f'  рідкі {"+".join(RARE_LETTERS)}: еталон '
      f'{sum(rf[c] for c in RARE_LETTERS):.4f}, випадковий текст {3 / M:.4f}, '
      f'поріг < {RARE_MAX}')


def score(text, alpha):
    f = letter_freq(text, alpha)
    return sum(f[c] for c in FREQ_LETTERS), sum(f[c] for c in RARE_LETTERS)


def attack(path, verbose=False):
    found = []
    for alpha in ALPHABETS:
        ct = clean(read(path), alpha)
        top_ct = [b for b, _ in bigram_freqs(ct, overlapping=False).most_common(5)]
        keys, rows = set(), []
        for X1, X2 in permutations(LANG_BIGRAMS, 2):
            for Y1, Y2 in permutations(top_ct, 2):
                dX = (bigram_to_num(X1, alpha) - bigram_to_num(X2, alpha)) % M2
                dY = (bigram_to_num(Y1, alpha) - bigram_to_num(Y2, alpha)) % M2
                sols = solve_congruence(dX, dY, M2)
                for a in sols:
                    if a % M == 0 or (a, 0) in keys:
                        continue
                    b = (bigram_to_num(Y1, alpha) - a * bigram_to_num(X1, alpha)) % M2
                    if (a, b) in keys:
                        continue
                    keys.add((a, b))
                    pt = decrypt(ct, a, b, alpha)
                    fr, ra = score(pt, alpha)
                    rows.append((X1, Y1, X2, Y2, len(sols), a, b, fr, ra,
                                 fr > FREQ_MIN and ra < RARE_MAX))
                    if fr > FREQ_MIN and ra < RARE_MAX:
                        found.append((alpha, a, b, fr, ra, pt, top_ct))
        if verbose:
            print(f'\nалфавіт ...щ{alpha[26]}{alpha[27]}эюя')
            print(f'  біграми ШТ: {", ".join(top_ct)}')
            print(f'  зіставлень {len(LANG_BIGRAMS) * 4 * len(top_ct) * 4}, '
                  f'різних ключів {len(keys)}, '
                  f'із кількома розв\'язками {sum(1 for r in rows if r[4] > 1)}')
            print(f'\n{"X*->Y*":>14}{"X**->Y**":>14}{"розв.":>7}{"a":>6}{"b":>6}'
                  f'{"часті":>8}{"рідкі":>8}{"":>5}')
            for X1, Y1, X2, Y2, ns, a, b, fr, ra, ok in rows[:10]:
                print(f'{X1 + "->" + Y1:>14}{X2 + "->" + Y2:>14}{ns:>7}{a:>6}'
                      f'{b:>6}{fr:>8.4f}{ra:>8.4f}{"  ПРИЙНЯТО" if ok else "":>5}')
            print(f'... ще {len(rows) - 10} рядків')
    return found


print(f'\nБіграми мови: {", ".join(LANG_BIGRAMS)}')
print('\n' + '=' * 72)
print(f'ВАРІАНТ {CIPHER}')
print('=' * 72)
for alpha, a, b, fr, ra, pt, top_ct in attack(CIPHER, verbose=True):
    print(f'\nКЛЮЧ a = {a}, b = {b}   алфавіт ...щ{alpha[26]}{alpha[27]}эюя')
    print(f'  часті {fr:.4f} > {FREQ_MIN},  рідкі {ra:.4f} < {RARE_MAX}')
    print(f'\n{pt[:500]}')
    open('decrypted_07.txt', 'w', encoding='utf-8').write(pt)

print('\n' + '=' * 72)
print(f'ТЕСТОВИЙ ФАЙЛ {TEST}')
print('=' * 72)
for alpha, a, b, fr, ra, pt, top_ct in attack(TEST, verbose=True):
    print(f'\nКЛЮЧ a = {a}, b = {b}   алфавіт ...щ{alpha[26]}{alpha[27]}эюя')
    print(f'  часті {fr:.4f} > {FREQ_MIN},  рідкі {ra:.4f} < {RARE_MAX}')
    print(f'\n{pt[:300]}')