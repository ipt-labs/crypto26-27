from common import M, M2, egcd, inverse, solve_congruence

print(f'm = {M},  m^2 = {M2}\n')

print('РОЗШИРЕНИЙ АЛГОРИТМ ЕВКЛІДА')
for a, b in ((240, 46), (200, 961), (31, 961)):
    g, x, y = egcd(a, b)
    print(f'  egcd({a}, {b}) = ({g}, {x}, {y})   перевірка: '
          f'{a}*{x} + {b}*{y} = {a * x + b * y}')

print('\nОБЕРНЕНИЙ ЕЛЕМЕНТ ЗА МОДУЛЕМ')
for a, n in ((200, M2), (3, M2), (31, M2), (62, M2)):
    inv = inverse(a, n)
    if inv is None:
        print(f'  {a}^-1 mod {n} не існує (gcd != 1)')
    else:
        print(f'  {a}^-1 mod {n} = {inv}   перевірка: {a}*{inv} mod {n} = '
              f'{a * inv % n}')

print('\nЛІНІЙНІ ПОРІВНЯННЯ ax = b (mod n)')
for a, b, n in ((6, 12, 18), (2, 3, 4), (200, 1, M2), (31, 62, M2), (14, 28, M2)):
    sols = solve_congruence(a, b, n)
    if not sols:
        print(f'  {a}x = {b} (mod {n}):  розв\'язків немає')
    else:
        print(f'  {a}x = {b} (mod {n}):  {len(sols)} розв\'язк(ів) -> '
              f'{sols if len(sols) <= 8 else sols[:8] + ["..."]}')
        assert all((a * s - b) % n == 0 for s in sols)
print('\nусі знайдені розв\'язки перевірено підстановкою')