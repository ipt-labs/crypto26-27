import random
from common import Decrypt, Encrypt, GenerateKeyPair, Sign, Verify

E = 65537
random.seed(7)

pr = dict(line.split(' = ') for line in open('primes.txt').read().splitlines())
pubA, privA = GenerateKeyPair(e=E, p=int(pr['p']), q=int(pr['q']))
pubB, privB = GenerateKeyPair(e=E, p=int(pr['p1']), q=int(pr['q1']))

for name, pub, priv, other_pub in (('A', pubA, privA, pubB),
                                   ('B', pubB, privB, pubA)):
    e, n = pub
    print(f'=== АБОНЕНТ {name} ===')
    print(f'n = {n}')
    print(f'e = {e}\n')

    M = random.randrange(2, min(n, other_pub[1]))
    print(f'ШИФРУВАННЯ для адресата (його відкритим ключем)')
    print(f'  M = {M}')
    C = Encrypt(M, other_pub)
    print(f'  C = Encrypt(M, pub_адресата) = {C}')
    M2 = Decrypt(C, privB if name == 'A' else privA)
    print(f'  M* = Decrypt(C, priv_адресата) = {M2}')
    print(f'  M* == M: {M2 == M}\n')

    print(f'ЦИФРОВИЙ ПІДПИС (власним секретним ключем)')
    S = Sign(M, priv)
    print(f'  S = Sign(M, priv_{name}) = {S}')
    print(f'  Verify(M, S, pub_{name}) = {Verify(M, S, pub)}')
    bad = (M + 1) % n
    print(f'  Verify(M+1, S, pub_{name}) = {Verify(bad, S, pub)}  (має бути False)\n')