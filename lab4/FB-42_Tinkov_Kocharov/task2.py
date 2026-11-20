import random
from common import GenerateKeyPair, egcd, power_mod

E = 65537
random.seed(7)

pr = dict(line.split(' = ') for line in open('primes.txt').read().splitlines())
pubA, privA = GenerateKeyPair(e=E, p=int(pr['p']), q=int(pr['q']))
pubB, privB = GenerateKeyPair(e=E, p=int(pr['p1']), q=int(pr['q1']))

for name, pub, priv in (('A', pubA, privA), ('B', pubB, privB)):
    e, n = pub
    d, p, q = priv
    print(f'=== АБОНЕНТ {name} ===')
    print(f'p = {p}')
    print(f'q = {q}')
    print(f'n = p*q = {n}')
    print(f'e = {e}')
    print(f'd = {d}')
    print(f'довжина n: {n.bit_length()} біт\n')

e, n = pubA
d, p, q = privA
phi = (p - 1) * (q - 1)
print('=== ПЕРЕВІРКА СПІВВІДНОШЕНЬ ДЛЯ ПАРИ КЛЮЧІВ A ===')
print(f'phi(n) = (p-1)(q-1) = {phi}')
print(f'n = p*q:                 {p * q == n}')
print(f'gcd(e, phi(n)) = 1:      {egcd(E, phi)[0] == 1}')
print(f'e*d mod phi(n) = 1:      {E * d % phi == 1}')
print(f'  e*d = {E * d}')
print(f'  e*d mod phi(n) = {E * d % phi}')
m = random.randrange(2, n)
c = power_mod(m, e, n)
print(f'\n(M^e)^d mod n = M:       {power_mod(c, d, n) == m}')
print(f'  M = {m}')
print(f'  C = {c}')
print(f'  M* = {power_mod(c, d, n)}')
print(f'\nn <= n1 (A <= B):        {pubA[1] <= pubB[1]}')