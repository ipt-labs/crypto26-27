from common import ALPHABETS, LANG_BIGRAMS, clean, read
from lab1_common import bigram_freqs, top_n

CIPHER = '07.txt'
REFERENCE = 'bratia_karamazovy.txt'

ct = clean(read(CIPHER))
cnt = bigram_freqs(ct, overlapping=False)

print(f'Шифртекст {CIPHER}: {len(ct)} літер, {sum(cnt.values())} біграм, '
      f'{len(cnt)} різних')
print('\nП\'ЯТЬ НАЙЧАСТІШИХ БІГРАМ ШИФРТЕКСТУ')
print(f'{"біграма":>9}{"кількість":>11}{"частота":>10}')
for bg, c, p in top_n(cnt, 5):
    print(f'{bg:>9}{c:>11}{p:>10.5f}')

ref = clean(read(REFERENCE, 'cp1251'))
rcnt = bigram_freqs(ref, overlapping=False)
order = [b for b, _ in rcnt.most_common()]
rtotal = sum(rcnt.values())

print(f'\nПЕРЕВІРКА ЧАСТИХ БІГРАМ МОВИ за текстом із практикуму №1')
print(f'({REFERENCE}: {len(ref)} літер, {rtotal} біграм)\n')
print(f'{"біграма":>9}{"кількість":>11}{"частота":>10}{"місце":>8}')
for bg, c, p in top_n(rcnt, 5):
    print(f'{bg:>9}{c:>11}{p:>10.5f}{order.index(bg) + 1:>8}')

print(f'\nБіграми, названі в методичці: {", ".join(LANG_BIGRAMS)}')
print(f'{"біграма":>9}{"кількість":>11}{"частота":>10}{"місце":>8}')
for bg in LANG_BIGRAMS:
    print(f'{bg:>9}{rcnt[bg]:>11}{rcnt[bg] / rtotal:>10.5f}'
          f'{order.index(bg) + 1:>8}')