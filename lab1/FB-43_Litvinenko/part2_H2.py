from math import log2
with open(r"C:\Users\Tuf\Desktop\3 Курс\Крипта\lab1\space", "r", encoding="utf-8") as file:
    space = file.read()
with open(r"C:\Users\Tuf\Desktop\3 Курс\Крипта\lab1\no_space", "r", encoding="utf-8") as file:
    no_space = file.read()

print("Довжина тексту з пробілами:", len(space))
print("Довжина тексту без пробілів:", len(no_space))


"============================"
#2. підрахунку частот біграм;
"============================"


#1) Для текста з пробілами 
#1.1 ті що перетинаються (зсув на 1 символ)
bigrams_with_space_p = {}
for i in range(len(space) - 1):
    if space[i:i+2] not in bigrams_with_space_p.keys():
        bigrams_with_space_p[space[i:i+2]] = 1
    else:
        bigrams_with_space_p[space[i:i+2]] += 1


#1.2 ті що не перетинаються (зсув на 2 символи) 
bigrams_with_space_np = {}
for i in range(0, len(space) - 1, 2):
    if space[i:i+2] not in bigrams_with_space_np.keys():
        bigrams_with_space_np[space[i:i+2]] = 1
    else:
        bigrams_with_space_np[space[i:i+2]] += 1

print("Сума частот біграм із перекриттям для файлу з пробілами:", sum(bigrams_with_space_p.values()))
print("Сума частот біграм без перекриття для файлу з пробілами:", sum(bigrams_with_space_np.values()))




#2) Для текста без пробілів
#2.1 ті що перетинаються (зсув на 1 символ)
bigrams_no_space_p = {}
for i in range(len(no_space) - 1):
    if no_space[i:i+2] not in bigrams_no_space_p.keys():
        bigrams_no_space_p[no_space[i:i+2]] = 1
    else:
        bigrams_no_space_p[no_space[i:i+2]] += 1


#2.2 ті що не перетинаються (зсув на 2 символи)
bigrams_no_space_np = {}
for i in range(0, len(no_space) - 1, 2):
    if no_space[i:i+2] not in bigrams_no_space_np.keys():
        bigrams_no_space_np[no_space[i:i+2]] = 1
    else:
        bigrams_no_space_np[no_space[i:i+2]] += 1

print("Сума частот біграм із перекриттям для файлу без пробілів:", sum(bigrams_no_space_p.values()))
print("Сума частот біграм без перекриття для файлу без пробілів:", sum(bigrams_no_space_np.values()))




"TOP 5"
#для файлу з пробілами, біграми що перекриваються (зсув на 1 символ)

print('--' * 20)
print('ТОП 5 БІГРАМ З ПЕРЕКРИТТЯМ, ДЛЯ ФАЙЛУ З ПРОБІЛАМИ')
print('--' * 20)

cop = bigrams_with_space_p.copy()
maximum = 0
max_key = ''
number_top = 1

while number_top <= 5:
    for i in cop:
        if cop[i] > maximum:
            maximum = cop[i]
            max_key = i
    cop.pop(max_key)
    print(f"ТОП {number_top}: ", max_key, maximum )
    number_top += 1
    maximum = 0

print('--' * 20)
print('ТОП 5 БІГРАМ БЕЗ ПЕРЕКРИТТЯ, ДЛЯ ФАЙЛУ З ПРОБІЛАМИ')
print('--' * 20)

cop = bigrams_with_space_np.copy()
maximum = 0
max_key = ''
number_top = 1

while number_top <= 5:
    for i in cop:
        if cop[i] > maximum:
            maximum = cop[i]
            max_key = i
    cop.pop(max_key)
    print(f"ТОП {number_top}: ", max_key, maximum )
    number_top += 1
    maximum = 0


#Для файлу без пробілів


print('--' * 20)
print('ТОП 5 БІГРАМ З ПЕРЕКРИТТЯМ, ДЛЯ ФАЙЛУ БЕЗ ПРОБІЛІВ')
print('--' * 20)


cop = bigrams_no_space_p.copy()
maximum = 0
max_key = ''
number_top = 1

while number_top <= 5:
    for i in cop:
        if cop[i] > maximum:
            maximum = cop[i]
            max_key = i
    cop.pop(max_key)
    print(f"ТОП {number_top}: ", max_key, maximum )
    number_top += 1
    maximum = 0



print('--' * 20)
print('ТОП 5 БІГРАМ БЕЗ ПЕРЕКРИТТЯМ, ДЛЯ ФАЙЛУ БЕЗ ПРОБІЛІВ')
print('--' * 20)


cop = bigrams_no_space_np.copy()
maximum = 0
max_key = ''
number_top = 1

while number_top <= 5:
    for i in cop:
        if cop[i] > maximum:
            maximum = cop[i]
            max_key = i
    cop.pop(max_key)
    print(f"ТОП {number_top}: ", max_key, maximum )
    number_top += 1
    maximum = 0



#ймовірність

#1) для файлу з пробілами

#біграми що перетинаються
N1 = sum(bigrams_with_space_p.values())
bigrams_with_space_p_imovirnist = {}
for i in bigrams_with_space_p:
    if i not in bigrams_with_space_p_imovirnist:
        bigrams_with_space_p_imovirnist[i] = bigrams_with_space_p[i] / N1

#біграми що не перетинаються
N2 = sum(bigrams_with_space_np.values())
bigrams_with_space_np_imovirnist = {}
for i in bigrams_with_space_np:
    if i not in bigrams_with_space_np_imovirnist:
        bigrams_with_space_np_imovirnist[i] = bigrams_with_space_np[i] / N2


#2) для файлу без пробілів

#біграми що перетинаються
N3 = sum(bigrams_no_space_p.values())
bigrams_no_space_p_imovirnist = {}
for i in bigrams_no_space_p:
    if i not in bigrams_no_space_p_imovirnist:
        bigrams_no_space_p_imovirnist[i] = bigrams_no_space_p[i] / N3

#біграми що не перетинаються
N4 = sum(bigrams_no_space_np.values())
bigrams_no_space_np_imovirnist = {}
for i in bigrams_no_space_np:
    if i not in bigrams_no_space_np_imovirnist:
        bigrams_no_space_np_imovirnist[i] = bigrams_no_space_np[i] / N4


#Ентропія H2

#1) для файлу з пробілами

H2_space_p = 0
for i in bigrams_with_space_p_imovirnist:
    H2_space_p -= bigrams_with_space_p_imovirnist[i]* log2(bigrams_with_space_p_imovirnist[i])

H2_space_np = 0
for i in bigrams_with_space_np_imovirnist:
    H2_space_np -= bigrams_with_space_np_imovirnist[i]* log2(bigrams_with_space_np_imovirnist[i])


#2) для файлу без пробілів
H2_no_space_p = 0
for i in bigrams_no_space_p_imovirnist:
    H2_no_space_p -= bigrams_no_space_p_imovirnist[i]* log2(bigrams_no_space_p_imovirnist[i])

H2_no_space_np = 0
for i in bigrams_no_space_np_imovirnist:
    H2_no_space_np -= bigrams_no_space_np_imovirnist[i]* log2(bigrams_no_space_np_imovirnist[i])

#Відповіді
print(f'H2 ДЛЯ ФАЙЛУ З ПРОБІЛАМИ, ДЛЯ БІГРАМ ЯКІ ПЕРЕТИНАЮТЬСЯ: {H2_space_p}')
print(f'H2 ДЛЯ ФАЙЛУ З ПРОБІЛАМИ, ДЛЯ БІГРАМ ЯКІ НЕ ПЕРЕТИНАЮТЬСЯ: {H2_space_np}')
print(f'H2 ДЛЯ ФАЙЛУ БЕЗ ПРОБІЛІВ, ДЛЯ БІГРАМ ЯКІ ПЕРЕТИНАЮТЬСЯ: {H2_no_space_p}')
print(f'H2 ДЛЯ ФАЙЛУ БЕЗ ПРОБІЛІВ, ДЛЯ БІГРАМ ЯКІ НЕ ПЕРЕТИНАЮТЬСЯ {H2_no_space_np}')
