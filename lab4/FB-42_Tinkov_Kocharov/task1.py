import random
from common import gen_prime, miller_rabin_trace

BITS = 256
random.seed(7)

log = []
p = gen_prime(BITS, log=log)
q = gen_prime(BITS, log=log)
p1 = gen_prime(BITS, log=log)
q1 = gen_prime(BITS, log=log)

if p * q > p1 * q1:
    p, q, p1, q1 = p1, q1, p, q

with open('primes.txt', 'w') as f:
    for name, value in (('p', p), ('q', q), ('p1', p1), ('q1', q1)):
        f.write(f'{name} = {value}\n')

print(f'Довжина простих чисел: {BITS} біт\n')
print(f'p  = {p}')
print(f'q  = {q}')
print(f'p1 = {p1}')
print(f'q1 = {q1}')
print(f'\nn  = p*q   = {p * q}')
print(f'n1 = p1*q1 = {p1 * q1}')
print(f'умова n <= n1: {p * q <= p1 * q1}')
print('\nпрості збережено у primes.txt')

print(f'\nКАНДИДАТИ, ЩО НЕ ПРОЙШЛИ ПЕРЕВІРКУ: {len(log)}')
for n, reason in log[:10]:
    print(f'  {n}')
    print(f'    -> {reason}')
if len(log) > 10:
    print(f'  ... ще {len(log) - 10}')

print('\nПРОМІЖНІ РЕЗУЛЬТАТИ ТЕСТУ МІЛЛЕРА-РАБІНА')
a = 2
d, s, steps, ok = miller_rabin_trace(p, a)
print(f'n = p = {p}')
print(f'основа a = {a}')
print(f'n - 1 = 2^{s} * {d}')
for name, val in steps:
    print(f'  {name}')
    print(f'    {val}')
print(f'висновок: {"n проходить тест (ймовірно просте)" if ok else "n складене"}')

print('\nперевірка складеного числа тим самим тестом:')
composite = p * q
d, s, steps, ok = miller_rabin_trace(composite, a)
print(f'n = p*q,  n - 1 = 2^{s} * d')
print(f'  x = a^d mod n = {steps[0][1]}')
print(f'  кроків піднесення до квадрата: {len(steps) - 1}')
print(f'висновок: {"проходить" if ok else "n складене"}')