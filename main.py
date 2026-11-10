import random
import msvcrt
import timeit

import unicodedata


def anne_bissextile(annee):
    return annee % 4 == 0 and annee % 100 != 0 or annee % 400 == 0

# print(anne_bissextile(2020))

def lanceur_de_balles():
    pret = bool(int(input("Etes-vous prêt ? 1 = oui / 00 = non ")))
    panier_vide = False

    if pret and not panier_vide:
        print("lancer de balle")

# lanceur_de_balles()

def distributeur_boissons():
    boissons = {'coca' : 10, 'fanta' : 3, 'eau' : 0}
    selection = input("veuillez choisir votre boisson (coca, fanta ou eau): ")
    if selection in boissons and boissons[selection] > 0:
        boissons[selection] -= 1
        return  f"Votre boisson {selection} est prete"
    return f"Votre boisson {selection} n'est pas disponible"

# print(distributeur_boissons())

def calculatrice():
    nbr1 = int(input("entrez un nombre: "))
    nbr2 = int(input("entrez un nombre: "))
    operateur = input("entrez un operateur: ")
    if operateur == "+":
        return nbr1 + nbr2
    elif operateur == "-":
        return nbr1 - nbr2
    elif operateur == "*":
        return nbr1 * nbr2
    elif operateur == "/":
        return nbr1 / nbr2
    else:
        return None

# print(calculatrice())

def note():
    note = int(input("entrez une note: "))
    if 20 < note < 0:
        return f"Votre note de {note} dois etre comprise entre 0 et 20"
    if note <= 10:
        return f"Votre note de {note} est insuffisante"
    elif 10 <= note < 20:
        return f"Votre note de {note} est bonne"
    elif note == 20:
        return f"Votre note de {note} est exellente"

# print(note())

def multi_2():
    nb = 1
    while nb <= 10:
        print(f"{nb} * 2 = {nb * 2}")
        nb += 1

# multi_2()

def lanceur_de_balles_2():
    pret = bool(int(input("Etes-vous prêt ? 1 = oui / 00 = non ")))
    panier = 3

    while panier > 0:
        if pret :
            panier -= 1
            print("lancer de balle")

# lanceur_de_balles_2()

def multi():
    nb1 = 1
    nb2 = 1
    while nb1 <= 10:
        while nb2 <= 10:
            print(f"{nb1} * {nb2} = {nb1 * nb2}")
            nb2 += 1
        nb1 += 1
        nb2 = 1
        print("*" * 20)

# multi()

def guest_num():
    guest_nb = random.randint(1, 100)
    num = int(input("entrez un nombre: "))
    while guest_nb != num:
        if num > guest_nb:
            print(f"{num} est plus petit")
            num = int(input("entrez un nombre: "))
        elif num < guest_nb:
            print(f"{num} est plus grand")
            num = int(input("entrez un nombre: "))
    print(f"c'est gagné")

# guest_num()

def list_6():
    result = []
    i = 1
    while i<= 6:
        entree = input("entrez un nombre: ")
        result.append(entree)
        i += 1
    print(result)

# list_6()

def list_10():
    result = []
    i = 1
    while len(result) < 10:
        entree = i * 2
        result.append(entree)
        i = entree
    print(result)

# list_10()

def moyenne():
    total = []
    nb_joueur = int(input("entrez un nombre de joueur: "))
    for i in range(nb_joueur):
        total.append(int(input("entrez le score du joueur: ")))
    print(f"la moyenne est de {sum(total) / nb_joueur}")

# moyenne()

def reverse_list(liste):
    print(liste[::-1])

# reverse_list([1,2,3,4,5])

def sort_list(liste):
    print(sorted(liste))

# sort_list([4,8,66,3,7,-1])

def f(liste1, liste2):
    liste3 = []
    for i in range(len(liste2) + len(liste1)):
        minimum1 = min(liste1, default=float('inf'))
        minimum2 = min(liste2, default=float('inf'))
        if minimum1 < minimum2:
            liste1.remove(minimum1)
            liste3.append(minimum1)
        else:
            liste2.remove(minimum2)
            liste3.append(minimum2)
    print(liste3)

# f([3,2,5,9],[1,6,8,4])

def exo27():
    liste = [0] * 10
    continu = True
    position = 0
    while continu:
        pass
    
    print(msvcrt.getch().decode("ASCII"))

# pion()

def exo29():
    tab = []
    for i  in range(10):
        tab.append(int(input("entrez un nombre: ")))
    return min(tab)

# print(exo29())

def exo30():
    tab = [1,4,8,10,11]
    numero = int(input("entrez un nombre: "))
    for i in range(len(tab)):
        if numero > tab[i]:
            continue
        else:
            tab.insert(i, numero)
            break
    return tab

# print(exo30())

def exo31():
    tab = [1,4,8,10,11]
    numero = int(input("entrez un nombre: "))
    for i in range(len(tab)):
        if numero == tab[i]:
            return True
    return False

# print(exo31())

def exo32(num):
    return num ** 2

def exo33(tab, taille, value):
    for i in range(taille):
        if value == tab[i]:
            return i
    return -1

def execTimeit(func):
    def wrapper(*args):
        time = timeit.timeit(lambda: func(*args), number=10000)
        print(f"Temps d'exécution: {time:.6f} sec")

    return wrapper

@execTimeit
def exo34(tab1,tab2):
    print(tab1 + tab2)
    # return tab1 + tab2

# (exo34([1,2],[3,4]))

def nettoyage(txt):
    nfkd_form = unicodedata.normalize('NFKD', txt.lower())
    return "".join([c for c in nfkd_form if unicodedata.category(c) != 'Mn'])

@execTimeit
def nb_voyelle(txt):
    txt = nettoyage(txt)
    print(txt)
    total = 0

    for i in txt:
        if i in ["a", "e", "i", "o", "u", "y"]:
            total += 1
    print(total)
    return total

# print(nb_voyelle("Ésope reste ici et se repose"))

# @execTimeit
def palindrome(txt):
    txt = nettoyage(txt).replace(" ", "")

    palindromes = {
        txt[i:j]
        for i in range(len(txt))
        for j in range(i + 2, len(txt) + 1)
        if txt[i:j] == txt[i:j][::-1]
    }
    return palindromes

text = "Ésope reste ici et se repose"
# result = palindrome(text)
# print(f"Nombre de palindromes uniques trouvés : {len(result)}")
# print("Liste :", sorted(result, key=len, reverse=True))
# print(timeit.timeit(lambda: palindrome(text), number=10000))

def pyramide(n):
    for i in range(1, 2 * n):
        print("* " * (i if i <= n else 2 * n - i))

# pyramide(5)

def pyramide2(n): [print("* " * (i if i <= n else 2 * n - i)) for i in range(1, 2 * n)]

print(timeit.timeit(lambda: pyramide2(3), number=1000))
print(timeit.timeit(lambda: pyramide(3), number=1000))


