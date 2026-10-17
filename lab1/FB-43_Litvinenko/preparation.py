ru = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж',
    'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
    'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц',
    'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'
]

with open(r"C:\Users\Tuf\Desktop\3 Курс\Крипта\lab1\laba1.txt.txt", 'r', encoding='utf-8') as f:
    file = f.read().lower()

start = list(file)
for i in range(len(start)):
    if start[i] not in ru:
        start[i] = " "

start1 = ''.join(start)
start1 = ' '.join(start1.split())
start_no_spaces = ''.join(start1.split())

with open(r"C:\Users\Tuf\Desktop\3 Курс\Крипта\lab1\space", 'w', encoding='utf-8') as file1:
    file1.write(start1)

with open(r"C:\Users\Tuf\Desktop\3 Курс\Крипта\lab1\no_space", 'w', encoding='utf-8') as file2:
    file2.write(start_no_spaces)