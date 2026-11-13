import random
from t1 import modular_exponentiation
from t23 import generate_prime_for_report, GenerateKeyPair

def text_to_int(text):
    return int.from_bytes(text.encode('utf-8'), byteorder='big')

def int_to_text(integer):
    byte_length = (integer.bit_length() + 7) // 8
    return integer.to_bytes(byte_length, byteorder='big').decode('utf-8')

def Encrypt(M, e, n):
    return modular_exponentiation(M, e, n)

def Decrypt(C, d, n):
    return modular_exponentiation(C, d, n)

def Sign(M, d, n):
    return modular_exponentiation(M, d, n)

def Verify(M, S, e, n):
    return modular_exponentiation(S, e, n) == M

def SendKey(k, e1, n1, d, n):
    # Абонент А підписує ключ k своїм секретним ключем
    S = Sign(k, d, n)
    # Абонент А шифрує сам ключ k відкритим ключем B
    k1 = Encrypt(k, e1, n1)
    # Абонент А шифрує свій підпис S відкритим ключем B
    S1 = Encrypt(S, e1, n1)
    return k1, S1

def ReceiveKey(k1, S1, d1, n1, e, n):
    # Абонент B розшифровує ключ k своїм секретним ключем
    k = Decrypt(k1, d1, n1)
    # Абонент B розшифровує підпис S своїм секретним ключем
    S = Decrypt(S1, d1, n1)
    # Абонент B перевіряє справжність підпису відкритим ключем A
    is_authentic = Verify(k, S, e, n)
    return k, is_authentic

if __name__ == "__main__":
    print("[*] Генеруємо ключі для Абонентів...")
    p_A, q_A = generate_prime_for_report(256, "p_A"), generate_prime_for_report(256, "q_A")
    p_B, q_B = generate_prime_for_report(256, "p_B"), generate_prime_for_report(256, "q_B")
    
    n_A, n_B = p_A * q_A, p_B * q_B
    if n_A > n_B:
        p_A, p_B = p_B, p_A
        q_A, q_B = q_B, q_A
        
    keys_A = GenerateKeyPair(p_A, q_A)
    keys_B = GenerateKeyPair(p_B, q_B)

    n, e, d = keys_A['public'][0], keys_A['public'][1], keys_A['private'][0]
    n1, e1, d1 = keys_B['public'][0], keys_B['public'][1], keys_B['private'][0]

    print("\n" + "="*43)
    print("Завдання 4. Шифрування та Цифровий підпис")
    print("="*43)
    text_message = "CryptaLab4VOfb43"
    M = text_to_int(text_message)
    print(f"Відкритий текст: '{text_message}'")
    print(f"Текст у вигляді числа (M): {M}\n")
    
    # Шифрування для Абонента B
    C = Encrypt(M, e1, n1)
    print(f"[ШИФРУВАННЯ] Криптограма (C), зашифрована ключем B:\n{C}\n")
    
    # Розшифрування Абонентом B
    decrypted_M = Decrypt(C, d1, n1)
    decrypted_text = int_to_text(decrypted_M)
    print(f"[РОЗШИФРУВАННЯ] Отримане число: {decrypted_M}")
    print(f"Розшифрований текст: '{decrypted_text}'")
    assert M == decrypted_M, "Помилка розшифрування!"
    
    print("\n--- Цифровий підпис ---")
    # Абонент А підписує повідомлення
    S = Sign(M, d, n)
    print(f"[ПІДПИС] Цифровий підпис (S), створений ключем A:\n{S}\n")
    
    # Абонент B перевіряє підпис
    is_valid = Verify(M, S, e, n)
    print(f"[ПЕРЕВІРКА] Результат перевірки підпису Абонентом B: {is_valid}")
    assert is_valid, "Помилка перевірки підпису!"

    print("\n" + "="*43)
    print("Завдання 5. Протокол розсилання ключів")
    print("="*43)
    k = random.randrange(1, n)
    print(f"Згенерований секретний симетричний ключ (k) для передачі:\n{k}\n")
    
    print("Відправка від А до B...")
    k1, S1 = SendKey(k, e1, n1, d, n)
    print(f"Зашифрований ключ (k1) для передачі по каналу:\n{k1}\n")
    print(f"Зашифрований підпис (S1) для передачі по каналу:\n{S1}\n")
    
    print("Отримання Абонентом B...")
    received_k, is_authentic = ReceiveKey(k1, S1, d1, n1, e, n)
    print(f"Розшифрований симетричний ключ:\n{received_k}\n")
    print(f"Автентичність підтверджено: {is_authentic}")
    assert k == received_k and is_authentic, "Помилка у протоколі розсилання ключів!"