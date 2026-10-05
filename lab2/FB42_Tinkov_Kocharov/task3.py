from collections import Counter
from common import (
    ALPHABET, IDX, M, RU_FREQ, blocks, clean, decrypt, index_of_coincidence,
    read, theoretical_ic,
)

R = 15
ROWS = 12
SUSPECT = 6
ORD = ['1-ша', '2-га', '3-тя']

ct = clean(read('variant7.txt'))
parts = blocks(ct, R)
lang = sorted(ALPHABET, key=lambda c: -RU_FREQ[c])

print(f'Період r = {R}, довжина фрагмента {len(parts[0])}')
print('Літери мови за спаданням імовірності (ЛР1): ' +
      ', '.join(f'{c}({RU_FREQ[c]:.5f})' for c in lang[:3]))

print('\n' + '=' * 70)
print('КРОК 1. k = (y* - x*) mod m,  x* = "о"')
print('=' * 70)
print(f'{"фрагмент":>9}{"y*":>5}{"N(y*)":>7}{"k":>4}')
key = ''
for i, b in enumerate(parts):
    y = Counter(b).most_common(1)[0]
    k = ALPHABET[(IDX[y[0]] - IDX['о']) % M]
    key += k
    print(f'{i:>9}{y[0]:>5}{y[1]:>7}{k:>4}')

pt = decrypt(ct, key)
print(f'\nКлюч: {key}')
print(f'Текст: {pt[:120]}')

print('\n' + '=' * 70)
print('КРОК 2. Аналіз розшифрованого тексту')
print('=' * 70)
print(f'Текст у рядках по {R} символів — стовпець = один фрагмент:\n')
print('     ' + ''.join(f'{i % 10}' for i in range(R)))
for row in range(ROWS):
    print(f'{row:>4} ' + pt[row * R:(row + 1) * R])
print(f'\nУ стовпці {SUSPECT} читаються неіснуючі сполучення '
      f'(прошлоШятнадцать, днейиЪтарый, постепОнно) — фрагмент {SUSPECT} '
      f'розшифровано невірно.')

print('\n' + '=' * 70)
print(f'КРОК 3. Для фрагмента {SUSPECT} беремо другу та третю літери мови')
print('=' * 70)
y = Counter(parts[SUSPECT]).most_common(1)[0][0]
for rank, x in enumerate(lang[:3]):
    k = ALPHABET[(IDX[y] - IDX[x]) % M]
    trial = key[:SUSPECT] + k + key[SUSPECT + 1:]
    frag = decrypt(ct, trial)[:60]
    print(f'\nx* = "{x}" ({ORD[rank]} за імовірністю)   k = {k}')
    print(f'  {frag}')
    print(f'  {"".join("^" if i % R == SUSPECT else " " for i in range(60))}')

CHOSEN = 'е'
k_fix = ALPHABET[(IDX[y] - IDX[CHOSEN]) % M]
KEY = key[:SUSPECT] + k_fix + key[SUSPECT + 1:]
print(f'\nЧитається лише варіант x* = "{CHOSEN}": "прошлопятнадцать",')
print(f'"днейистарый", "постепенно". Приймаємо k = {k_fix} для фрагмента '
      f'{SUSPECT}.')

print('\n' + '=' * 70)
print('КРОК 4. Перевірка')
print('=' * 70)
pt = decrypt(ct, KEY)
print(f'ВІДНОВЛЕНИЙ КЛЮЧ: {KEY}')
print(f'I(ВТ) = {index_of_coincidence(pt):.5f}   '
      f'I мови = {theoretical_ic():.5f}   I0 = {1 / M:.5f}')
print(f'\n{pt[:400]}')
open('decrypted.txt', 'w', encoding='utf-8').write(pt)