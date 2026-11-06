alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
text = open("text_8.txt", encoding="utf-8").read()
key = open("key.txt", encoding="utf-8").read()
wrong_key = "ф" + key[1:]

def decrypt(text, key):
    return "".join(alphabet[(alphabet.index(c) - alphabet.index(key[i % len(key)])) % 32]
        for i, c in enumerate(text)
    )

correct = decrypt(text, key)
wrong = decrypt(text, wrong_key)
positions = [
    i + 1 for i, (a, b) in enumerate(zip(correct, wrong))
    if a != b
]
results = [
    f"Правильний ключ: {key}",
    f"Ключ із помилкою: {wrong_key}",
    f"Кількість змінених літер: {len(positions)} із {len(text)}",
    f"Частка змінених літер: {len(positions) / len(text):.4%}",
    f"Перші 15 позицій помилок: {positions[:15]}",
    f"Остання позиція помилки: {positions[-1]}",
    f"Позиції відповідають прогнозу: "
    f"{positions == list(range(1, len(text) + 1, len(key)))}",
    "",
    "Порівняння фрагментів по 20 літер:",
    "Правильно | Із помилкою"
]
for i in range(0, 100, 20):
    results.append(f"{correct[i:i + 20]} | {wrong[i:i + 20]}")
result = "\n".join(results)
print(result)
open("decoded_8_wrong.txt", "w", encoding="utf-8").write(wrong)
open("results_task4.txt", "w", encoding="utf-8").write(result)
