"""
Перевірка власної реалізації RSA на тестовому середовищі
http://asymcryptwebservice.appspot.com/?section=rsa

Ключі абонентів А і В беруться з key_A.json / key_B.json (створюються gen_RSA_pair.py).
Відкритий ключ сервера запам'ятовується один раз командою `server`.

Приклади:
  python site_interop.py keys
  python site_interop.py server --n <Modulus> --e <Public exponent>

  # а) власне шифрування -> розшифрування на сервері
  python site_interop.py encrypt --random                       # шифрує для сервера
  # б) шифрування на сервері (розділ Encryption, ключ абонента А) -> розшифрування тут
  python site_interop.py decrypt --who A --c <Ciphertext>

  python site_interop.py sign   --who A --random                # підпис -> сайт, розділ Verification
  python site_interop.py verify --msg <Message> --sig <Signature>   # підпис сервера (розділ Signature)

  python site_interop.py send-key    --who A --random-key       # А -> сервер (сайт: Receive Key)
  python site_interop.py receive-key --who B --key <Key> --sig <Signature>   # сервер -> В (сайт: Send Key)
"""
import argparse
import json
import os
import sys

from protocol import *

SERVER_FILE = os.path.join(BASE_DIR, "server_key.json")


def load_private(name):
    return GetKeyPairs()["AB".index(name)][0]


def load_public(name):
    if name == "server":
        if not os.path.exists(SERVER_FILE):
            raise ValueError("Спершу збережіть відкритий ключ сервера: "
                             "python site_interop.py server --n <Modulus> --e <Public exponent>")
        with open(SERVER_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return int(data["n"], 16), int(data["e"], 16)
    return GetKeyPairs()["AB".index(name)][1]


def random_message(modulus, num_bytes=32):
    num_bytes = max(1, min(num_bytes, (modulus.bit_length() - 1) // 8))
    return generate_random_hex_message(num_bytes)


def get_message(args, modulus):
    if args.text is not None:
        return args.text.encode("utf-8").hex()
    if args.msg is not None:
        return args.msg
    return random_message(modulus)


def show_text(hex_value):
    try:
        text = bytes.fromhex(int_to_hex(hex_to_int(hex_value))).decode("utf-8")
        if text.isprintable():
            print(f"  як UTF-8 текст: {text}")
    except (ValueError, UnicodeDecodeError):
        pass


def show_public(name, public_key):
    n, e = public_key
    print(f"Modulus (hex):         {int_to_hex(n)}")
    print(f"Public exponent (hex): {int_to_hex(e)}")


def cmd_keys(args):
    for name in "AB":
        print(f"--- Відкритий ключ абонента {name} (для полів Modulus / Public exponent на сайті) ---")
        show_public(name, load_public(name))
        print(f"Довжина n: {load_public(name)[0].bit_length()} біт\n")


def cmd_server(args):
    n, e = hex_to_int(args.n), hex_to_int(args.e)
    with open(SERVER_FILE, "w", encoding="utf-8") as f:
        json.dump({"n": f"{n:x}", "e": f"{e:x}"}, f, indent=2)
    print(f"Відкритий ключ сервера збережено ({n.bit_length()} біт, e = {e}).")


def cmd_encrypt(args):
    public_key = load_public(args.to)
    message_hex = get_message(args, public_key[0])
    cipher_hex = Encrypt(message_hex, public_key)
    print(f"Одержувач: {args.to}")
    print(f"Повідомлення M (hex):            {message_hex}")
    print(f"Шифротекст C = M^e mod n (hex):  {cipher_hex}")
    if args.to == "server":
        kind = "Text" if args.text is not None else "Bytes"
        print(f"\nНа сайті: розділ Decryption -> Ciphertext = C, {kind} -> Decrypt. Має повернутись M.")


def cmd_decrypt(args):
    message_hex = Decrypt(args.c, load_private(args.who))
    print(f"Абонент {args.who} розшифровує за допомогою свого секретного ключа")
    print(f"Шифротекст C (hex):                {int_to_hex(hex_to_int(args.c))}")
    print(f"Повідомлення M = C^d mod n (hex):  {message_hex}")
    show_text(message_hex)


def cmd_sign(args):
    private_key = load_private(args.who)
    message_hex = get_message(args, private_key[1] * private_key[2])
    message_hex, signature_hex = Sign(message_hex, private_key)
    print(f"Абонент {args.who} підписує своїм секретним ключем")
    print(f"Повідомлення M (hex):         {message_hex}")
    print(f"Підпис S = M^d mod n (hex):   {signature_hex}")
    print("\nНа сайті: розділ Verification -> Message = M (Bytes), Signature = S, Modulus і Public exponent:")
    show_public(args.who, load_public(args.who))
    print("Verify має повернути true.")


def cmd_verify(args):
    result = Verify((args.msg, args.sig), load_public(args.by))
    print(f"Перевірка підпису відкритим ключем ({args.by}): {result}")


def cmd_send_key(args):
    private_key = load_private(args.who)
    public_key = load_public(args.to)
    n = private_key[1] * private_key[2]
    k_hex = args.k if args.k is not None else int_to_hex(random.randint(1, n - 1))
    k1_hex, S1_hex = SendKey(k_hex, private_key, public_key, verbose=True)
    if args.to == "server":
        print("\nНа сайті: розділ Receive Key -> Key = k1, Signature = S1, Modulus і Public exponent абонента "
              f"{args.who} (відправника):")
        show_public(args.who, load_public(args.who))
        print("Receive має повернути Key = k і Verification = true.")


def cmd_receive_key(args):
    private_key = load_private(args.who)
    public_key = load_public(args.sender)
    k_hex, is_verified = ReceiveKey((args.key, args.sig), private_key, public_key, verbose=True)
    print(f"\nОтриманий ключ k (hex): {k_hex}")
    print(f"Підпис відправника ({args.sender}) підтверджено: {is_verified}")


def peer(value):
    return "server" if value.lower() == "server" else value.upper()


def build_parser():
    parser = argparse.ArgumentParser(description="Перевірка реалізації RSA на сайті asymcryptwebservice.appspot.com",
                                     formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    who = lambda p: p.add_argument("--who", choices=["A", "B"], type=str.upper, required=True, help="абонент (власник ключа)")

    def message_args(p):
        group = p.add_mutually_exclusive_group()
        group.add_argument("--msg", help="повідомлення M, hex")
        group.add_argument("--text", help="повідомлення M як текст (UTF-8)")
        group.add_argument("--random", action="store_true", help="випадкове повідомлення (за замовчуванням)")

    sub.add_parser("keys", help="показати відкриті ключі А і В").set_defaults(func=cmd_keys)

    p = sub.add_parser("server", help="запам'ятати відкритий ключ сервера з розділу Server Key")
    p.add_argument("--n", required=True, help="Modulus, hex")
    p.add_argument("--e", required=True, help="Public exponent, hex")
    p.set_defaults(func=cmd_server)

    p = sub.add_parser("encrypt", help="Encrypt: зашифрувати повідомлення відкритим ключем одержувача")
    message_args(p)
    p.add_argument("--to", choices=["server", "A", "B"], type=peer,
                   default="server", help="одержувач (за замовчуванням server)")
    p.set_defaults(func=cmd_encrypt)

    p = sub.add_parser("decrypt", help="Decrypt: розшифрувати криптограму секретним ключем А або В")
    who(p)
    p.add_argument("--c", required=True, help="Ciphertext, hex")
    p.set_defaults(func=cmd_decrypt)

    p = sub.add_parser("sign", help="Sign: підписати повідомлення секретним ключем А або В")
    who(p)
    message_args(p)
    p.set_defaults(func=cmd_sign)

    p = sub.add_parser("verify", help="Verify: перевірити підпис відкритим ключем (за замовчуванням - сервера)")
    p.add_argument("--msg", required=True, help="Message, hex")
    p.add_argument("--sig", required=True, help="Signature, hex")
    p.add_argument("--by", choices=["server", "A", "B"], type=peer,
                   default="server", help="чиїм відкритим ключем перевіряти (за замовчуванням server)")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("send-key", help="SendKey: протокол розсилання ключа, роль відправника")
    who(p)
    p.add_argument("--k", help="секретний ключ k, hex (за замовчуванням - випадковий 0 < k < n)")
    p.add_argument("--random-key", action="store_true", help="випадковий k (поведінка за замовчуванням)")
    p.add_argument("--to", choices=["server", "A", "B"], type=peer,
                   default="server", help="одержувач (за замовчуванням server)")
    p.set_defaults(func=cmd_send_key)

    p = sub.add_parser("receive-key", help="ReceiveKey: протокол розсилання ключа, роль одержувача")
    who(p)
    p.add_argument("--key", required=True, help="k1 (поле Key на сайті), hex")
    p.add_argument("--sig", required=True, help="S1 (поле Signature на сайті), hex")
    p.add_argument("--from", dest="sender", choices=["server", "A", "B"],
                   type=peer,
                   default="server", help="відправник, чий відкритий ключ перевіряє підпис (за замовчуванням server)")
    p.set_defaults(func=cmd_receive_key)
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    try:
        args.func(args)
    except ValueError as error:
        print(f"Помилка: {error}")
        sys.exit(2)
