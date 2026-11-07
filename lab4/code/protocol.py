from rsa import *
import random


def SendKey(k_hex, private_key_A, public_key_B, verbose = False):
    d_A, p_A, q_A = private_key_A
    n_A = p_A * q_A
    n_B, e_B = public_key_B

    if n_B < n_A:
        raise ValueError("Порушено обов'язкову умову протоколу: має виконуватись n1 >= n.")

    k_int = hex_to_int(k_hex)
    if not (0 < k_int < n_A):
        raise ValueError("Ключ k повинен задовольняти умову 0 < k < n.")

    _, S_hex = Sign(k_hex, private_key_A)
    k1_hex = Encrypt(k_hex, public_key_B)
    S1_hex = Encrypt(S_hex, public_key_B)

    if verbose:
        print("=== ЕТАП ВІДПРАВНИКА (Абонент А) ===")
        print(f"Випадковий секретний ключ k (hex):            {k_hex}")
        print(f"Підпис S = k^d mod n (hex):                   {S_hex}")
        print(f"Криптограма ключа k1 = k^e1 mod n1 (hex):     {k1_hex}")
        print(f"Криптограма підпису S1 = S^e1 mod n1 (hex):   {S1_hex}")
        print("Справжність відправника: підпис S створено секретним ключем d абонента А.")
        print("Конфіденційність: k і S зашифровано відкритим ключем (e1, n1) абонента В.")

    return k1_hex, S1_hex


def ReceiveKey(encrypted_package, private_key_B, public_key_A, verbose = False):
    k1_hex, S1_hex = encrypted_package
    d_B, p_B, q_B = private_key_B
    n_B = p_B * q_B
    n_A, e_A = public_key_A

    if n_B < n_A:
        raise ValueError("Порушено обов'язкову умову протоколу: має виконуватись n1 >= n.")

    k_hex = Decrypt(k1_hex, private_key_B)
    S_hex = Decrypt(S1_hex, private_key_B)
    is_verified = Verify((k_hex, S_hex), public_key_A)

    k_int = hex_to_int(k_hex)
    if not (0 < k_int < n_A):
        is_verified = False

    if verbose:
        S_int = hex_to_int(S_hex)
        k_check_hex = int_to_hex(pow(S_int, e_A, n_A))
        print("\n=== ЕТАП ОТРИМУВАЧА (Абонент В) ===")
        print(f"Розшифрований ключ k = k1^d1 mod n1 (hex):   {k_hex}")
        print(f"Розшифрований підпис S = S1^d1 mod n1 (hex): {S_hex}")
        print(f"Перевірка підпису S^e mod n (hex):           {k_check_hex}")
        print(f"Результат перевірки справжності (k == S^e):  {is_verified}")
        print("Конфіденційність: розшифрувати k1, S1 може лише абонент В - власник секретного ключа d1.")
        print("Справжність відправника: підпис перевірено відкритим ключем (e, n) абонента А.")

    return k_hex, is_verified


if __name__ == "__main__":
    private_key_A, public_key_A = GetKeyPairs()[0]
    private_key_B, public_key_B = GetKeyPairs()[1]

    n_A, e_A = public_key_A
    n_B, e_B = public_key_B

    print("=== ПАРАМЕТРИ АБОНЕНТІВ ===")
    print(f"\nПублічний ключ абонента А (n, e): ({int_to_hex(n_A)}, {int_to_hex(e_A)})")
    print(f"\nПриватний ключ абонента А (d, p, q): ({int_to_hex(private_key_A[0])}, {int_to_hex(private_key_A[1])}, {int_to_hex(private_key_A[2])})\n")
    print(f"\nПублічний ключ абонента В (n1, e1): ({int_to_hex(n_B)}, {int_to_hex(e_B)})")
    print(f"\nПриватний ключ абонента В (d1, p1, q1): ({int_to_hex(private_key_B[0])}, {int_to_hex(private_key_B[1])}, {int_to_hex(private_key_B[2])})\n")
    print(f"Умова n <= n1 виконується: {n_A <= n_B}\n")

    k_int = random.randint(1, n_A - 1)
    k_hex = int_to_hex(k_int)

    encrypted_package = SendKey(k_hex, private_key_A, public_key_B, verbose=True)

    received_k_hex, is_authentic = ReceiveKey(encrypted_package, private_key_B, public_key_A, verbose=True)

    print("\n=== ПІДСУМОК РОБОТИ ПРОТОКОЛУ ===")
    print(f"Початковий ключ k == Отриманий ключ k: {k_hex == received_k_hex}")
    print(f"Підпис відправника А підтверджено:     {is_authentic}")
