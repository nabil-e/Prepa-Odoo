# FICHES DE RÉVISION : ALGORITHMIC PATTERNS (PYTHON)

---

## 📝 FICHE 1 : Pointeur de Lecture / Écriture (In-place Two Pointers)

### 📌 Le Concept
Utilisé pour modifier un tableau **directement sur place** sans allouer de mémoire supplémentaire (Espace O(1)).
* Un pointeur de **Lecture** (`read`) inspecte chaque élément un par un.
* Un pointeur d'**Écriture** (`write`) reste en arrière et n'avance que pour écraser/enregistrer les données valides.

### ⏱️ Complexité
* **Temporelle :** O(N) — Un seul passage à travers le tableau.
* **Spatiale :** O(1) — Aucune structure de données supplémentaire.

### 💻 Code Exemple (Modèle Analogue)
```python
def filtrer_elements_sur_place(arr, valeur_interdite):
    write = 0
    for read in range(len(arr)):
        if arr[read] != valeur_interdite:
            arr[write] = arr[read]
            write += 1
    return write  # Retourne la nouvelle taille effective du tableau
```

### 🎯 Exercices Cibles LeetCode
* `Move Zeroes`
* `Merge Sorted Array` (Astuce : Écrivez en partant de la fin !)
* `Squares of a Sorted Array`

---

## 📝 FICHE 2 : La Pile (Stack - LIFO)

### 📌 Le Concept
Une structure de données **Dernier Entré, Premier Sorti** (Last In, First Out). En Python, on utilise une simple liste `[]`.
* `.append(x)` pour empiler.
* `.pop()` pour dépiler le dernier élément inséré.
* Indispensable dès qu'un élément actuel dépend, s'annule ou se combine avec l'élément immédiatement précédent.

### ⏱️ Complexité
* **Temporelle :** O(N) — Chaque élément est empilé/dépilé au maximum une fois.
* **Spatiale :** O(N) — Dans le pire des cas, la pile stocke tous les éléments.

### 💻 Code Exemple (Modèle Analogue)
```python
def effacer_caracteres_annulables(chaine):
    stack = []
    for char in chaine:
        if char == "*" and stack:
            stack.pop()  # Annule le précédent
        elif char != "*":
            stack.append(char)
    return "".join(stack)
```

### 🎯 Exercices Cibles LeetCode
* `Valid Parentheses`
* `Remove All Adjacent Duplicates In String`
* `Baseball Game`
* `Backspace String Compare`

---

## 📝 FICHE 3 : Table de Hachage & Ensemble (Hash Map / Set)

### 📌 Le Concept
Exploiter les ensembles `set()` ou les dictionnaires `dict()` pour mémoriser des éléments ou leurs fréquences. L'avantage absolu est que la recherche d'un élément (`if x in mon_set`) s'exécute en temps constant O(1).

### ⏱️ Complexité
* **Temporelle :** O(N) — Un parcours pour remplir la structure, puis accès instantanés.
* **Spatiale :** O(N) — Stockage proportionnel au nombre d'éléments uniques.

### 💻 Code Exemple (Modèle Analogue)
```python
def trouver_doublons(tableau):
    deja_vus = set()
    doublons = set()
    for num in tableau:
        if num in deja_vus:
            doublons.add(num)
        deja_vus.add(num)
    return list(doublons)
```

### 🎯 Exercices Cibles LeetCode
* `Check if the Sentence Is Pangram`
* `Intersection of Two Arrays`
* `First Unique Character in a String`

---

## 📝 FICHE 4 : Deux Pointeurs Indépendants (Two Inputs)

### 📌 Le Concept
Placer un pointeur distinct au début de deux structures de données différentes (chaînes ou tableaux différents). On fait avancer les pointeurs de manière asynchrone selon qu'un critère de correspondance ou de comparaison est validé ou non.

### ⏱️ Complexité
* **Temporelle :** O(N + M) — Où N et M sont les tailles respectives des deux structures.
* **Spatiale :** O(1) — On ne stocke que deux variables d'indexation (les pointeurs).

### 💻 Code Exemple (Modèle Analogue)
```python
def sequence_commune(str1, str2):
    p1, p2 = 0, 0
    while p1 < len(str1) and p2 < len(str2):
        if str1[p1] == str2[p2]:
            p1 += 1
        p2 += 1
    return p1 == len(str1)
```

### 🎯 Exercices Cibles LeetCode
* `Is Subsequence`
