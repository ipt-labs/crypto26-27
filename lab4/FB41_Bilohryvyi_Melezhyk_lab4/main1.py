import random
from prime import gen_prime, miller_rabin, gcd
from rsa import gen_keys, encrypt, decrypt, sign, verify, send_key, receive_key

BITS = 256


def pair(bad):
    p = gen_prime(BITS, bad)
    q = gen_prime(BITS, bad)
    while q == p:
        q = gen_prime(BITS, bad)
    return p, q


print("=== Міллер-Рабін, один крок ===")
miller_rabin(gen_prime(BITS), k=1, log=True)

bad = []
p, q = pair(bad)
p1, q1 = pair(bad)
if p * q > p1 * q1:
    p, q, p1, q1 = p1, q1, p, q

print("\n=== прості числа ===")
for name, v in [("p", p), ("q", q), ("p1", p1), ("q1", q1)]:
    print(f"{name} = {v:x}")
print(f"відкинуто кандидатів: {len(bad)}")
for b in bad[:5]:
    print("  ", f"{b:x}")

pub_a, priv_a = gen_keys(p, q)
pub_b, priv_b = gen_keys(p1, q1)
n, e = pub_a
d = priv_a[0]
print("\n=== ключі A ===")
print(f"n = {n:x}\ne = {e:x}\nd = {d:x}")
print("ключі B:")
print(f"n1 = {pub_b[0]:x}\ne1 = {pub_b[1]:x}\nd1 = {priv_b[0]:x}")

phi = (p - 1) * (q - 1)
print("\n=== перевірка співвідношень (A) ===")
print("p, q прості:", miller_rabin(p, 40), miller_rabin(q, 40))
print("n = p*q:", n == p * q)
print("gcd(e, phi) == 1:", gcd(e, phi) == 1)
print("e*d mod phi == 1:", e * d % phi == 1)

m = random.randrange(1, n)
print("\n=== шифрування / підпис ===")
print(f"M = {m:x}")
for name, pub, priv in [("A", pub_a, priv_a), ("B", pub_b, priv_b)]:
    c = encrypt(m, pub)
    s = sign(m, priv)
    print(f"\n{name}:")
    print(f"C = {c:x}")
    print("розшифровано вірно:", decrypt(c, priv) == m)
    print(f"S = {s:x}")
    print("підпис вірний:", verify(m, s, pub))

k = random.randrange(1, n)
k1, s1 = send_key(k, priv_a, pub_b)
print("\n=== розсилання ключа A -> B (Штабний режим) ===")
print(f"k  = {k:x}")
print(f"k1 = {k1:x}")
print(f"S1 = {s1:x}")
res = receive_key(k1, s1, priv_b, pub_a)
print(f"B отримав k = {res:x}" if res is not None else "підпис не пройшов")
print("збігається:", res == k)


print("\n=== ІМІТАЦІЯ АТАКИ: ")
s1_spoiled = s1 + 1  
print(f"Зіпсований S1 = {s1_spoiled:x}")

res_spoiled = receive_key(k1, s1_spoiled, priv_b, pub_a)

if res_spoiled is None:
    print(" ПІДПИС НЕ ПРОЙШО")
else:
    print(f"люч помилково прийнято: {res_spoiled:x}")