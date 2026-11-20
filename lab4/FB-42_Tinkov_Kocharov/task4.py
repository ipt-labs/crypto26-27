import random
from common import GenerateKeyPair, ReceiveKey, SendKey, power_mod

E = 65537
random.seed(7)

pr = dict(line.split(' = ') for line in open('primes.txt').read().splitlines())
pubA, privA = GenerateKeyPair(e=E, p=int(pr['p']), q=int(pr['q']))
pubB, privB = GenerateKeyPair(e=E, p=int(pr['p1']), q=int(pr['q1']))

eA, nA = pubA
dA, pA, qA = privA
eB, nB = pubB
dB, pB, qB = privB

print('ПРОТОКОЛ КОНФІДЕНЦІЙНОГО РОЗСИЛАННЯ КЛЮЧІВ  A -> B\n')
print(f'n  (A) = {nA}')
print(f'n1 (B) = {nB}')
print(f'умова n <= n1: {nA <= nB}\n')

k = random.randrange(2, nA)
print(f'A обирає секретний ключ k:\n  k = {k}\n')

print('A обчислює та передає:')
S = power_mod(k, dA, nA)
print(f'  S  = k^d mod n       = {S}')
k1, S1 = SendKey(k, privA, pubB)
print(f'  k1 = k^e1 mod n1     = {k1}')
print(f'  S1 = S^e1 mod n1     = {S1}')
print(f'\n  у відкритий канал іде пара (k1, S1)\n')

print('B обчислює:')
k_recv, k_dec, S_dec = ReceiveKey(k1, S1, privB, pubA)
print(f'  k = k1^d1 mod n1     = {k_dec}')
print(f'  S = S1^d1 mod n1     = {S_dec}')
print(f'  перевірка підпису: S^e mod n = {power_mod(S_dec, eA, nA)}')
print(f'  збігається з k:      {power_mod(S_dec, eA, nA) == k_dec}')
print(f'\n  ReceiveKey повернув: {k_recv}')
print(f'  отриманий ключ збігається з надісланим: {k_recv == k}\n')

print('АТАКА: зловмисник підміняє підпис')
fake_S1 = (S1 + 1) % nB
k_bad, _, _ = ReceiveKey(k1, fake_S1, privB, pubA)
print(f'  ReceiveKey(k1, S1+1, ...) = {k_bad}  (None = підпис не пройшов)')

print('\nЯКИЙ КЛЮЧ ЩО ЗАБЕЗПЕЧУЄ')
print('  конфіденційність  — відкритий ключ e1 абонента B: лише власник d1')
print('                      може зняти шифрування з k1 та S1;')
print('  справжність       — секретний ключ d абонента A: підпис S = k^d mod n')
print('                      перевіряється відкритим e, і підробити його без d')
print('                      неможливо.')