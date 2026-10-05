from common import (
    ALPHABET, M, RU_FREQ, clean, decrypt, encrypt, frequencies,
    index_of_coincidence, read, theoretical_ic,
)

KEYS = ['да', 'кот', 'мира', 'книга', 'библиотекарь', 'шелестстраниц',
        'тишинавчитальномзале']

plain = clean(read('plain_raw.txt'))
open('plain_clean.txt', 'w', encoding='utf-8').write(plain)

print(f'Довжина ВТ: {len(plain)} символів\n')

print(f'{"літера":>8}{"частота мови (ЛР1)":>22}{"частота ВТ":>14}')
own = frequencies(plain)
for c in sorted(ALPHABET, key=lambda x: -RU_FREQ[x]):
    print(f'{c:>8}{RU_FREQ[c]:>22.5f}{own[c]:>14.5f}')

print(f'\nТеоретичний I для російської мови (за частотами ЛР1): {theoretical_ic():.5f}')
print(f'I0 = 1/m = 1/{M}: {1 / M:.5f}')
print(f'I власного ВТ: {index_of_coincidence(plain):.5f}')

print(f'\n{"Ключ":<22}{"r":>4}{"I":>10}')
print(f'{"(відкритий текст)":<22}{"-":>4}{index_of_coincidence(plain):>10.5f}')

for key in KEYS:
    ct = encrypt(plain, key)
    assert decrypt(ct, key) == plain
    open(f'cipher_r{len(key)}.txt', 'w', encoding='utf-8').write(ct)
    print(f'{key:<22}{len(key):>4}{index_of_coincidence(ct):>10.5f}')
    print('   ', ct[:60])