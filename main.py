import numpy as np
import random
from typing import List
import math

info = np.loadtxt('_info-data-discrete.txt', dtype="str")
plik_type = np.loadtxt('australian-type.txt', dtype="str")
plik = np.loadtxt("australian.txt", dtype="str")


print("3 Dane z pliku z typami")
print(plik_type)
print("3a) istniejące klassy decyzyjne")
all_symbole_decyzyjne=""
symbole_decyzyjne=""
liczba_obiektow = 0
for i in range(len(plik)):
    all_symbole_decyzyjne += str((plik[i][-1]))
    liczba_obiektow += 1

symbole_decyzyjne += all_symbole_decyzyjne[0]
for i in range(1, len(all_symbole_decyzyjne)):
    tmp = all_symbole_decyzyjne[i]
    flaga = 0
    for j in range(len(symbole_decyzyjne)):
        if tmp == symbole_decyzyjne[j]:
            flaga += 1
    if flaga == 0:
        symbole_decyzyjne += tmp

for i in range(len(symbole_decyzyjne)):
    print(symbole_decyzyjne[i])

print("\nb) Wielkość klas decyzyjnych")
print(liczba_obiektow)

decision_classes = np.genfromtxt("_info-data-discrete.txt", dtype="str")


print("\nc) Minimalne i maksymalne wartości poszczególnych atrybutów")
liczba_obiektow = len(plik)
for j in range(len(plik_type)):
    if "n" == plik_type[j][1]:
        wartosci = [float(plik[i][j]) for i in range(len(plik))]
        atr_name = "atr" + str(j+1)
        print(f"{atr_name} max: {max(wartosci)} min: {min(wartosci)}")


#3d
print("\nd) Liczba różnych dostępnych wartości")
for j in range(len(plik_type)):
    rozne = []
    sprawdz = set()
    istniejace = []
    for i in range(len(plik)):
        rozne.append((plik[i][j]))
    for c in rozne:
        if c not in sprawdz:
            sprawdz.add(c)
            istniejace.append(c)
    print("atr" + str(j + 1) + "  ilosc: " + str(len(istniejace)))


print("\ne) Lista wszystkich różnych dostępnych wartości")
for j in range(len(plik_type)):
    rozne = []
    sprawdz = set()
    istniejace = []
    for i in range(len(plik)):
        rozne.append((plik[i][j]))
    for c in rozne:
        if c not in sprawdz:
            sprawdz.add(c)
            istniejace.append(c)
    print(f"atr{j+1}")
    print(*istniejace, sep=" ")
    print()


#3f

def string_to_double(s: str) -> float:
    try:
        return float(s)
    except ValueError:
        return 0.0


def odchylenie(list: List[float], srednia: float, ilosc: int) -> float:
    wariacja = sum(math.pow(c - srednia, 2) / ilosc for c in list)
    return math.sqrt(wariacja)


print("\nf) Odchylenie standardowe dla każdego atrybutu w całym systemie")
for j in range(len(plik_type)):
    rozne = [string_to_double(plik[i][j]) for i in range(len(plik))]
    srednia = sum(rozne) / len(rozne)
    odchylenie_std = odchylenie(rozne, srednia, len(plik))
    print(f"Atr{j + 1} Odchylenie standardowe: {odchylenie_std}")



print("4 zad")

def generate_missing_values(plik, plik_type):
    nieznane = []
    for j in range(len(plik_type)):
        if "n" == plik_type[j][1]:
            for i in range(len(plik)):
                nieznane.append(plik[i][j])

    procent_10 = int(0.1 * len(nieznane))
    for i in range(procent_10):
        index = random.randint(0, len(nieznane)-1)
        if nieznane[index] == "?":
            i -= 1
        else:
            nieznane[index] = "?"

    atr = len(nieznane) // len(plik)
    seria = 0
    srednia_n = 0
    for i in range(atr):
        for j in range(seria, len(plik) + seria):
            if nieznane[j] != "?":
                srednia_n += float(nieznane[j])
        srednia_n = srednia_n / len(plik)
        for a in range(seria, len(plik) + seria):
            if nieznane[a] == "?":
                nieznane[a] = str(srednia_n)
        srednia_n = 0
        seria += len(plik)

    print("\na) wygeneruj dziesięć procent brakujących danych w wybranym systemie decyzyjnym")
    print("i uzupełnij brakujące wartości najczęściej spotykanymi wartościami lub wartościami średnimi dla atrybutów symbolicznych")


#4a
generate_missing_values(plik, plik_type)

#4b

def normalizacja(obj, min_val, max_val, a, b):
    ai_obj = (((obj - min_val) * (b - a)) / (max_val - min_val)) + a
    return ai_obj

print("\nb) Znornalizuj atrybuty numeryczne wybranego systemu na przedziały: (normalize attribute values into intervals): < −1,1 >, < 0,1 >, < −10,10 >\n")

for j in range(len(plik_type)):
    if "n" == plik_type[j][1]:
        for i in range(len(plik)):
            data = [string_to_double(plik[i][j]) for i in range(len(plik))]
        max_val = max(data)
        min_val = min(data)
        kontrola = 0
        print(f"Atr{j+1} po normalizacji")
        for c in data:
            ai_obj1 = normalizacja(c, min_val, max_val, -1, 1)
            print("{:.2f} ".format(ai_obj1), end="")
            kontrola += 1
            if kontrola == 10:
                kontrola = 0
                break
        print("\n")
        for c in data:
            ai_obj2 = normalizacja(c, min_val, max_val, 0, 1)
            print("{:.2f} ".format(ai_obj2), end="")
            kontrola += 1
            if kontrola == 10:
                kontrola = 0
                break
        print("\n")
        for c in data:
            ai_obj3 = normalizacja(c, min_val, max_val, -10, 10)
            print("{:.2f} ".format(ai_obj3), end="")
            kontrola += 1
            if kontrola == 10:
                kontrola = 0
                break
        data.clear()
        print("\n\n")

#4c
def Standaryzacja(x, mean, std_dev):
    return (x - mean) / std_dev


def Odchylenie(data, mean, n):
    return np.sqrt(sum([(x - mean) ** 2 for x in data]) / (n - 1))


def standaryzacja(obj, srednia, odchylenie):
    ai_obj = (obj - srednia) / odchylenie
    return ai_obj


print("\nc) Dokonaj standaryzacji wartości numerycznych wybranego systemu decyzyjnego\n")
standaryzacja_lst = []
for j in range(len(plik_type)):
    if "n" == plik_type[j][1]:
        for i in range(len(plik)):
            standaryzacja_lst = [string_to_double(plik[i][j]) for i in range(len(plik))]
        srednia = sum(standaryzacja_lst) / len(standaryzacja_lst)
        odchylenie = Odchylenie(standaryzacja_lst, srednia, len(plik))
        print(f"Atr{j+1} po standaryzacji")
        for i in range(len(standaryzacja_lst)):
            ai_obj = standaryzacja(standaryzacja_lst[i], srednia, odchylenie)
            standaryzacja_lst[i] = ai_obj
        odch = Odchylenie(standaryzacja_lst, sum(standaryzacja_lst) / len(standaryzacja_lst), len(plik))
        print(f"\nSrednia po standaryzacji: {sum(standaryzacja_lst)/len(standaryzacja_lst):.0f}")
        print(f"\nOdchylenie po standaryzacji: {odch}")
        print("\n\n")
        standaryzacja_lst.clear()

for i in range(len(plik)):
    for j in range(len(plik[i])):
        print(plik[i][j], end=" ")
    print()


print("\nMariusz Raś, Dawid Sójka IIGR  IO\n")
