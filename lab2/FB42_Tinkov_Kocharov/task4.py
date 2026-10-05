from common import ALPHABET, IDX, M, clean, decrypt, read

KEY = 'арудазовархимаг'
POS = 4
NEW = 'е'

r = len(KEY)
ct = clean(read('variant7.txt'))
bad_key = KEY[:POS] + NEW + KEY[POS + 1:]
shift = (IDX[KEY[POS]] - IDX[NEW]) % M

print(f'Правильний ключ: {KEY}')
print(f'Змінений ключ:   {bad_key}   (символ {POS}: {KEY[POS]} -> {NEW})')

print('\nПРОГНОЗ ДО ЕКСПЕРИМЕНТУ')
print(f'  ПЕРІОДИЧНІСТЬ: неправильно розшифрується лише фрагмент {POS},')
print(f'  тобто кожен {r}-й символ — 1/{r} = {1 / r:.1%} тексту; решта')
print(f'  {r - 1} фрагментів не постраждають, текст залишиться читабельним.')
print(f'  ХАРАКТЕР: спотворення не випадкові. При дешифруванні ключ')
print(f'  віднімається, тому кожен символ фрагмента {POS} зсунеться за')
print(f'  алфавітом на ту саму сталу величину {IDX[KEY[POS]]} - {IDX[NEW]} = '
      f'{shift} (mod {M}),')
print(f'  тобто фрагмент буде зашифрований шифром Цезаря з ключем {shift}.')

good = decrypt(ct, KEY)
bad = decrypt(ct, bad_key)

print('\nРЕЗУЛЬТАТ ЕКСПЕРИМЕНТУ')
print(f'Розшифрування правильним ключем:\n{good[:150]}')
print(f'\nРозшифрування зміненим ключем:\n{bad[:150]}')

print(f'\nТекст рядками по {r} символів (стовпець = фрагмент):\n')
print('     ' + ''.join(f'{i % 10}' for i in range(r)))
for row in range(8):
    print(f'{row:>4} ' + bad[row * r:(row + 1) * r])

diff = [i for i in range(len(good)) if good[i] != bad[i]]
shifts = {(IDX[bad[i]] - IDX[good[i]]) % M for i in diff}

print('\nПОРІВНЯННЯ З ПРОГНОЗОМ')
print(f'  ПЕРІОДИЧНІСТЬ')
print(f'    усі {len(diff)} відмінностей лежать у фрагменті {POS}: '
      f'{all(i % r == POS for i in diff)}')
print(f'    частка спотворених символів: {len(diff)}/{len(good)} = '
      f'{len(diff) / len(good):.1%}   (прогноз {1 / r:.1%})')
print(f'  ХАРАКТЕР')
print(f'    множина зсувів усіх спотворених символів: {shifts}   '
      f'(прогноз {{{shift}}})')
print(f'    приклади заміни:', end=' ')
seen = []
for i in diff:
    pair = f'{good[i]}->{bad[i]}'
    if pair not in seen:
        seen.append(pair)
    if len(seen) == 6:
        break
print(', '.join(seen))

