import random
from common import (
    Decrypt, Encrypt, GenerateKeyPair, ReceiveKey, SendKey, Sign, Verify,
)

E = 65537
random.seed(7)

pr = dict(line.split(' = ') for line in open('primes.txt').read().splitlines())
pubA, privA = GenerateKeyPair(e=E, p=int(pr['p']), q=int(pr['q']))
pubB, privB = GenerateKeyPair(e=E, p=int(pr['p1']), q=int(pr['q1']))

SERVER_N = 0x82C7C76E8BF610BA2DBF42FDA452E263B9BFCD39C6514857D621C4169F6D5119654F0D4588639ED5550F71C7F95716822FFCAED0746582B8A1482B5515D9D7EA62DE3B576C7FD807F7FF21E014C4A926E041F00857A7F3E3BD3D3BB12106E334B0835230A237BB2AB8B5B03C7754BEC7598B35B6656BA857FA11254A7B6C8049
SERVER_E = 0x10001
SERVER_CIPHERTEXT = 0x14EE30DBEB681BFF8D13050A74B3B9ECF03DDAAF2419813F1487E07A1606088379CC9C5ECBA47EC616DEA044E01D917A192186E66458EF08F2BFDD1022597B92
SERVER_MESSAGE = 0x48656C6C6F
SERVER_SIGNATURE = 0x37D0ABED558E89AA8ED01F7B300E202301DDEAAEB483D931FC86E5C0475E1F561BEC7E969EA42D993F059640932C4D89D8C8198D23A563BCE08702549F7C48AA2C48CCE64C0C8ADFC733AC65EC3D6D34E937A51224D18EF597547066EB56836BFAFCFC9072F655E3053C8808B83E2798FB27D6BEBED142EE55233D7422D1C5D7
SERVER_K1 = 0x4A98553397697D95D1966B32F0625E202E7CBED4A9D4E2C73DBA37A21D1025FAAD18F60269ECEEC1C083C62601FE4083AACC3050637A8ABD3173CB4F9DBC4500
SERVER_S1 = 0x60EE87F2D669C1A3F83F80C2BE3A5AA916A478D763163142A9CB28729BFDAC2231403A1E82689F7DB6951FC880792A13E91BE8D540A516B2DC49F1AC288F782C
SERVER_N6 = 0x853BAB32CDBBA9D1A8ECCC59FD76166AF8FB6CC62340503D46884FEF6F5C5F19
SERVER_E6 = 0x10001


def h(x):
    return format(x, 'X')


def smaller_pair(limit):
    bits = (limit.bit_length() - 2) // 2
    while True:
        pub, priv = GenerateKeyPair(bits=bits, e=E)
        if pub[1] < limit:
            return pub, priv


eA, nA = pubA
print('=== НАШІ КЛЮЧІ ДЛЯ ВВЕДЕННЯ НА СЕРВЕРІ ===')
print(f'modulus  (n) = {h(nA)}')
print(f'exponent (e) = {h(eA)}')
print(f'довжина n: {nA.bit_length()} біт')
if SERVER_N:
    print(f'довжина n сервера: {SERVER_N.bit_length()} біт')
    print(f'n сервера {"<" if SERVER_N < nA else ">="} наш n')
print()

limit = min(nA, SERVER_N) if SERVER_N else nA
M = random.randrange(2, limit)

print('=== 1. ШИФРУВАННЯ: наша реалізація -> сервер ===')
print(f'M = {h(M)}')
if SERVER_N:
    C = Encrypt(M, (SERVER_E, SERVER_N))
    print(f'C = Encrypt(M, відкритий ключ сервера) = {h(C)}')
    print('   -> вставити C у поле Decrypt на сервері, має вийти M')
else:
    print('   заповніть SERVER_N та SERVER_E')

print('\n=== 2. ШИФРУВАННЯ: сервер -> наша реалізація ===')
if SERVER_CIPHERTEXT:
    M2 = Decrypt(SERVER_CIPHERTEXT, privA)
    print(f'C від сервера = {h(SERVER_CIPHERTEXT)}')
    print(f'M = Decrypt(C, наш секретний ключ) = {h(M2)}')
else:
    print('   заповніть SERVER_CIPHERTEXT')

print('\n=== 3. ПІДПИС: наша реалізація -> сервер ===')
S = Sign(M, privA)
print(f'M = {h(M)}')
print(f'S = Sign(M, наш секретний ключ) = {h(S)}')
print('   -> вставити M, S і наш відкритий ключ у Verify на сервері')

print('\n=== 4. ПІДПИС: сервер -> наша реалізація ===')
if SERVER_SIGNATURE and SERVER_N:
    ok = Verify(SERVER_MESSAGE, SERVER_SIGNATURE, (SERVER_E, SERVER_N))
    print(f'M від сервера = {h(SERVER_MESSAGE)}')
    print(f'S від сервера = {h(SERVER_SIGNATURE)}')
    print(f'Verify(M, S, відкритий ключ сервера) = {ok}')
else:
    print('   заповніть SERVER_MESSAGE, SERVER_SIGNATURE, SERVER_N, SERVER_E')

print('\n=== 5. ПЕРЕДАЧА КЛЮЧА: наша реалізація -> сервер ===')
if SERVER_N:
    if SERVER_N >= nA:
        pubS, privS = pubA, privA
        print('умова n <= n1 виконана для нашої основної пари')
    else:
        pubS, privS = smaller_pair(SERVER_N)
        print(f'n сервера ({SERVER_N.bit_length()} біт) менший за наш '
              f'({nA.bit_length()} біт): умова n <= n1 порушена,')
        print('тому для відправника згенеровано пару з меншим модулем')
        print(f'modulus  (n) відправника = {h(pubS[1])}')
        print(f'exponent (e) відправника = {h(pubS[0])}')
        print(f'довжина n відправника: {pubS[1].bit_length()} біт')
        print('   -> саме цей відкритий ключ вводиться на сервері '
              'для перевірки підпису')
    k = random.randrange(2, pubS[1])
    k1, S1 = SendKey(k, privS, (SERVER_E, SERVER_N))
    print(f'k  = {h(k)}')
    print(f'k1 = {h(k1)}')
    print(f'S1 = {h(S1)}')
    print('   -> передати k1 і S1 серверу, він має відновити k')
else:
    print('   заповніть SERVER_N та SERVER_E')

n6 = SERVER_N6 or SERVER_N
e6 = SERVER_E6 or SERVER_E

print('\n=== 6. ПЕРЕДАЧА КЛЮЧА: сервер -> наша реалізація ===')
if SERVER_K1 and n6:
    print(f'довжина n сервера у цьому кроці: {n6.bit_length()} біт')
    if nA >= n6:
        pubR, privR = pubA, privA
    elif pubB[1] >= n6:
        pubR, privR = pubB, privB
        print('наш основний модуль менший за модуль сервера,')
        print('тому отримувачем виступає друга наша пара')
        print(f'modulus  (n) отримувача = {h(pubR[1])}')
        print(f'exponent (e) отримувача = {h(pubR[0])}')
    else:
        pubR, privR = None, None
        print(f'   модуль сервера ({n6.bit_length()} біт) більший '
              f'за обидва наші: умова n <= n1 не виконується,')
        print('   згенеруйте на сервері коротший ключ '
              'і впишіть його у SERVER_N6, SERVER_E6')
    if privR is not None:
        k_recv, k_dec, S_dec = ReceiveKey(SERVER_K1, SERVER_S1, privR,
                                          (e6, n6))
        print(f'k1 від сервера = {h(SERVER_K1)}')
        print(f'S1 від сервера = {h(SERVER_S1)}')
        print(f'k = {h(k_dec)}')
        print(f'підпис сервера перевірено: {k_recv is not None}')
else:
    print('   заповніть SERVER_K1, SERVER_S1 і (за потреби) SERVER_N6, SERVER_E6')