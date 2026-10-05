from common import (
    M, blocks, clean, encrypt, index_of_coincidence, read, theoretical_ic,
)

MAX_R = 35
ALTERNATIVES = [15, 30, 5, 10, 3, 4, 29]

ct = clean(read('variant7.txt'))
n = len(ct)
I_lang = theoretical_ic()
I0 = 1 / M
I_ct = index_of_coincidence(ct)

print(f'Довжина ШТ: {n} символів')
print(f'I(ШТ) = {I_ct:.5f}')
print(f'I мови = {I_lang:.5f}, I0 = 1/{M} = {I0:.5f}')

print('\n' + '=' * 64)
print('МЕТОД 1, АЛГОРИТМ 2. Порівняння I(ШТ) з Ir власних шифртекстів')
print('=' * 64)
plain = clean(read('plain_raw.txt'))
print(f'{"r":>4}{"Ir":>12}{"|Ir - I(ШТ)|":>16}')
for key in ['да', 'кот', 'мира', 'книга', 'библиотекарь', 'шелестстраниц',
            'тишинавчитальномзале']:
    ir = index_of_coincidence(encrypt(plain, key))
    print(f'{len(key):>4}{ir:>12.5f}{abs(ir - I_ct):>16.5f}')

print('\n' + '=' * 64)
print('МЕТОД 1, АЛГОРИТМ 1. Середній індекс відповідності блоків')
print('=' * 64)
print(f'{"r":>4}{"сер. I":>10}{"довж. блоку":>13}')
ic_by_r = {}
for r in range(1, MAX_R + 1):
    ic_by_r[r] = sum(index_of_coincidence(b) for b in blocks(ct, r)) / r
    print(f'{r:>4}{ic_by_r[r]:>10.5f}{n // r:>13}')

print('\n' + '=' * 64)
print('МЕТОД 2. Статистика співпадінь D(r)')
print('=' * 64)
print(f'{"r":>4}{"D(r)":>8}{"D(r)/(n-r)":>13}')
d_by_r = {}
for r in range(1, MAX_R + 1):
    d = sum(1 for i in range(n - r) if ct[i] == ct[i + r])
    d_by_r[r] = d / (n - r)
    print(f'{r:>4}{d:>8}{d_by_r[r]:>13.5f}')

print('\n' + '=' * 64)
print('КАНДИДАТИ: індекси відповідності по кожному блоку')
print('=' * 64)
for r in ALTERNATIVES:
    vals = [index_of_coincidence(b) for b in blocks(ct, r)]
    near_lang = sum(1 for v in vals if abs(v - I_lang) < abs(v - I0))
    print(f'\nr = {r}   довжина блоку {n // r}   сер. I = {sum(vals)/r:.5f}'
          f'   D(r)/(n-r) = {d_by_r[r]:.5f}')
    print('  I блоків: ' + ' '.join(f'{v:.4f}' for v in vals[:15]) +
          (' ...' if r > 15 else ''))
    print(f'  min {min(vals):.5f}   max {max(vals):.5f}')
    print(f'  блоків ближче до I мови, ніж до I0: {near_lang} з {r}')