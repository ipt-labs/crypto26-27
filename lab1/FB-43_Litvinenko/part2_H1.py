from math import log2
with open(r"C:\Users\Tuf\Desktop\3 Курс\Крипта\lab1\space", "r", encoding="utf-8") as file:
    space = file.read()
with open(r"C:\Users\Tuf\Desktop\3 Курс\Крипта\lab1\no_space", "r", encoding="utf-8") as file:
    no_space = file.read()

"=================================="
#підрахунку частот окремих символів
"=================================="

#for space
result_space = {}
for i in space:
    if i not in result_space.keys():
        result_space[i] = 1
    else:
        result_space[i] = result_space[i] + 1
res_space = sum(result_space.values())

#for no space
result_no_space = {}
for i in no_space:
    if i not in result_no_space.keys():
        result_no_space[i] = 1
    else:
        result_no_space[i] = result_no_space[i] + 1 
res_no_space = sum(result_no_space.values())


#for space
N = len(space)
prob_space = {}
for i in result_space:
    if i not in prob_space.keys():
        prob_space[i] = result_space[i] / N

#for no space
N = len(no_space)
prob_no_space = {}
for i in result_no_space:
    if i not in prob_no_space.keys():
        prob_no_space[i] = result_no_space[i] / N

"=================================="
#H1
"=================================="

#for space
H1_space = 0
for i in prob_space.values():
    H1_space += (i * log2(i))*-1
print(f"Енртропія Н1 для тексту з пробілами: {H1_space}")

#for no space
H1_no_space = 0
for j in prob_no_space.values():
    H1_no_space += (j * log2(j))*-1
print(f"Енртропія Н1 для тексту без пробілів: {H1_no_space}")


"Підрахунок символів"

print('--' * 20)
print('ТОП 5 СИМОВЛІВ ДЛЯ ФАЙЛУ З ПРОБІЛАМИ')
print('--' * 20)

cop = result_space.copy()
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
print('ТОП 5 СИМОВЛІВ ДЛЯ ФАЙЛУ БЕЗ ПРОБІЛІВ')
print('--' * 20)

cop = result_no_space.copy()
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