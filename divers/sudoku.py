"""
SUDOKU EN CONSOLE — fichier unique, sans bibliothèque externe.

Ce que fait le programme, en résumé
-----------------------------------
1. L'ordinateur fabrique une grille de sudoku COMPLÈTE et valide, au hasard.
2. Il enlève des chiffres un par un, en vérifiant à chaque fois que la grille
   n'a toujours qu'UNE SEULE solution possible (sinon il remet le chiffre).
3. Le joueur se déplace dans la grille avec les flèches et tape les chiffres
   directement dans les cases.

Comment le fichier est organisé
-------------------------------
- PARTIE 1 : la logique du sudoku (règles, résolution, génération).
- PARTIE 2 : le clavier et l'affichage dans la console.
- PARTIE 3 : la boucle de jeu (on lit une touche, on agit, on réaffiche).

Vocabulaire utilisé dans le code
--------------------------------
- grille   : liste de 9 listes de 9 entiers. 0 veut dire « case vide ».
- l, c     : numéro de ligne et de colonne, de 0 à 8 (0 = première).
- bloc     : un des 9 carrés de 3x3 cases, numérotés de 0 à 8.
- candidat : un chiffre qu'on a le droit de mettre dans une case vide.
- backtracking (retour sur trace) : on essaie un chiffre ; si on finit bloqué
  plus loin, on revient en arrière et on essaie le chiffre suivant.
"""

import os
import random
import sys

TAILLE = 9
"""Une grille de sudoku fait 9 cases de côté."""

CHIFFRES = range(1, 10)
"""Les chiffres autorisés : 1 à 9."""

DIFFICULTES = {"facile": 40, "moyen": 32, "difficile": 26}
"""Nombre de chiffres laissés dans la grille selon la difficulté.
Moins il y a de chiffres de départ, plus c'est difficile."""


# ===========================================================================
# PARTIE 1 : la logique du sudoku
# ===========================================================================

def num_bloc(l, c):
    """Donne le numéro (0 à 8) du bloc 3x3 qui contient la case (l, c).

    Les blocs sont numérotés de gauche à droite, puis de haut en bas :
        0 1 2
        3 4 5
        6 7 8
    Exemple : la case (4, 7) est dans le bloc 5 (milieu-droite).
    """
    return (l // 3) * 3 + c // 3


class Contraintes:
    """Mémorise quels chiffres sont déjà utilisés dans chaque ligne,
    chaque colonne et chaque bloc.

    Pourquoi ? Pour savoir si un chiffre est autorisé dans une case, il faudrait
    sinon relire toute la ligne, toute la colonne et tout le bloc à chaque fois.
    Ici, on garde 27 petits ensembles (9 lignes + 9 colonnes + 9 blocs) et la
    vérification devient instantanée.

    Il faut juste penser à appeler `ajouter` quand on pose un chiffre
    et `retirer` quand on l'enlève, pour que les ensembles restent à jour.
    """

    def __init__(self, grille):
        """Construit les ensembles à partir des chiffres déjà présents dans la grille."""
        self.lignes = [set() for _ in range(TAILLE)]
        self.colonnes = [set() for _ in range(TAILLE)]
        self.blocs = [set() for _ in range(TAILLE)]
        for l in range(TAILLE):
            for c in range(TAILLE):
                if grille[l][c]:
                    self.ajouter(l, c, grille[l][c])

    def possible(self, l, c, v):
        """Renvoie True si le chiffre v peut aller en (l, c) selon les règles :
        il ne doit être ni dans la ligne, ni dans la colonne, ni dans le bloc."""
        return (v not in self.lignes[l]
                and v not in self.colonnes[c]
                and v not in self.blocs[num_bloc(l, c)])

    def candidats(self, l, c):
        """Renvoie la liste des chiffres autorisés dans la case (l, c)."""
        return [v for v in CHIFFRES if self.possible(l, c, v)]

    def ajouter(self, l, c, v):
        """Note que le chiffre v vient d'être posé en (l, c)."""
        self.lignes[l].add(v)
        self.colonnes[c].add(v)
        self.blocs[num_bloc(l, c)].add(v)

    def retirer(self, l, c, v):
        """Note que le chiffre v vient d'être enlevé de (l, c)."""
        self.lignes[l].discard(v)
        self.colonnes[c].discard(v)
        self.blocs[num_bloc(l, c)].discard(v)


def _resoudre(grille, cont, vides, limite, aleatoire, compteur):
    """Cœur du programme : remplit la grille par backtracking.

    Principe, à chaque appel :
      1. S'il n'y a plus de case vide, on a trouvé une solution : on la compte.
      2. Sinon, on choisit la case vide qui a le MOINS de chiffres possibles.
         (Astuce classique : c'est là qu'on a le moins de chances de se tromper,
         ce qui accélère énormément la recherche.)
      3. On essaie chaque chiffre possible dans cette case, puis on rappelle la
         fonction pour remplir le reste (récursivité).
      4. Si ça mène à une impasse, on efface le chiffre et on essaie le suivant.

    Paramètres :
        grille    : la grille à remplir (elle est modifiée directement).
        cont      : l'objet Contraintes qui correspond à cette grille.
        vides     : liste des cases encore vides, sous forme (l, c).
        limite    : on s'arrête dès qu'on a trouvé ce nombre de solutions.
        aleatoire : si True, les chiffres sont essayés dans un ordre au hasard
                    (sert à créer des grilles différentes à chaque partie).
        compteur  : liste d'un seul élément, [nombre de solutions trouvées].
                    On utilise une liste pour pouvoir la modifier depuis
                    n'importe quel appel récursif.

    Renvoie True quand la limite de solutions est atteinte (on arrête tout).
    Dans ce cas, la grille reste remplie avec la dernière solution trouvée.
    """
    if not vides:
        compteur[0] += 1
        return compteur[0] >= limite

    # Recherche de la case vide la plus contrainte (le moins de candidats)
    meilleur_i, meilleurs_cands = 0, None
    for i, (l, c) in enumerate(vides):
        cands = cont.candidats(l, c)
        if meilleurs_cands is None or len(cands) < len(meilleurs_cands):
            meilleur_i, meilleurs_cands = i, cands
            if len(cands) <= 1:
                break  # impossible de faire mieux, inutile de chercher plus loin
    if not meilleurs_cands:
        return False  # impasse : une case n'accepte aucun chiffre

    l, c = vides.pop(meilleur_i)
    if aleatoire:
        random.shuffle(meilleurs_cands)

    for v in meilleurs_cands:
        grille[l][c] = v                      # on essaie v...
        cont.ajouter(l, c, v)
        if _resoudre(grille, cont, vides, limite, aleatoire, compteur):
            vides.insert(meilleur_i, (l, c))
            return True
        cont.retirer(l, c, v)                 # ...échec : on revient en arrière
        grille[l][c] = 0

    vides.insert(meilleur_i, (l, c))          # on remet la liste dans son état initial
    return False


def cases_vides(grille):
    """Renvoie la liste des cases vides (valeur 0), sous forme de couples (l, c)."""
    return [(l, c) for l in range(TAILLE) for c in range(TAILLE) if grille[l][c] == 0]


def compter_solutions(grille, limite=2):
    """Compte combien de solutions a une grille, sans la modifier.

    On s'arrête à `limite` (2 par défaut) : pour savoir si une solution est
    UNIQUE, il suffit de savoir s'il en existe au moins 2. Inutile de toutes
    les trouver, ce serait beaucoup plus long.

    Renvoie 0 (aucune solution), 1 (solution unique) ou 2 (plusieurs).
    """
    copie = [ligne[:] for ligne in grille]
    compteur = [0]
    _resoudre(copie, Contraintes(copie), cases_vides(copie), limite, False, compteur)
    return compteur[0]


def generer_grille_complete():
    """Fabrique une grille entièrement remplie et valide, différente à chaque appel.

    Astuce : on « résout » une grille vide en essayant les chiffres au hasard.
    """
    grille = [[0] * TAILLE for _ in range(TAILLE)]
    _resoudre(grille, Contraintes(grille), cases_vides(grille), 1, True, [0])
    return grille


def generer_puzzle(nb_indices):
    """Crée une grille à résoudre qui a une seule solution.

    Étapes :
      1. On génère une grille complète : ce sera la solution.
      2. On parcourt les cases dans un ordre au hasard et on essaie de vider
         chacune.
      3. Si, une fois la case vidée, la grille a plusieurs solutions, on remet
         le chiffre (il est indispensable). Sinon, on le laisse enlevé.
      4. On s'arrête quand il ne reste plus que `nb_indices` chiffres.

    Renvoie un couple (puzzle, solution) :
        puzzle   : la grille avec des trous, que le joueur doit compléter.
        solution : la grille complète correspondante.
    """
    solution = generer_grille_complete()
    puzzle = [ligne[:] for ligne in solution]

    positions = [(l, c) for l in range(TAILLE) for c in range(TAILLE)]
    random.shuffle(positions)
    restants = TAILLE * TAILLE

    for l, c in positions:
        if restants <= nb_indices:
            break
        sauvegarde = puzzle[l][c]
        puzzle[l][c] = 0
        if compter_solutions(puzzle, limite=2) != 1:
            puzzle[l][c] = sauvegarde
        else:
            restants -= 1

    return puzzle, solution


# ===========================================================================
# PARTIE 2 : clavier et affichage
# ===========================================================================

# Codes ANSI : de petites séquences de texte que la console interprète comme
# des ordres (changer de couleur, effacer l'écran, cacher le curseur...).
RESET = "\033[0m"              # revient au style normal
GRAS = "\033[1m"
INVERSE = "\033[7m"            # inverse texte et fond (sert à montrer le curseur)
CYAN = "\033[36m"
ROUGE = "\033[31m"
JAUNE = "\033[33m"
VERT = "\033[32m"
CACHER_CURSEUR = "\033[?25l"
MONTRER_CURSEUR = "\033[?25h"
EN_HAUT = "\033[H"             # replace l'écriture en haut à gauche de l'écran
EFFACER_ECRAN = "\033[2J"
EFFACER_FIN = "\033[J"         # efface tout ce qui suit sur l'écran

BORD = "+-------+-------+-------+"
AIDE = [
    "Flèches   : se déplacer",
    "1-9       : placer un chiffre",
    "0 / Suppr : effacer",
    "i : indice    v : vérifier",
    "s : solution  q : quitter",
]

# Lire UNE touche sans attendre Entrée se fait différemment selon le système.
# On définit donc la fonction lire_touche() en deux versions ; Python ne garde
# que celle qui correspond à l'ordinateur sur lequel il tourne.

if os.name == "nt":
    import msvcrt

    os.system("")  # astuce : active les codes ANSI dans la console Windows

    TOUCHES_SPECIALES = {"H": "HAUT", "P": "BAS", "K": "GAUCHE", "M": "DROITE", "S": "EFFACER"}
    """Sous Windows, une flèche envoie 2 caractères : '\\xe0' puis une lettre.
    Ce dictionnaire traduit cette lettre en nom de touche."""

    def lire_touche():
        """Attend qu'une touche soit pressée et renvoie son nom (version Windows).

        Renvoie "HAUT", "BAS", "GAUCHE", "DROITE", "ENTREE", "ECHAP" ou
        "EFFACER" pour les touches spéciales, sinon le caractère tapé ("5", "q"...).
        """
        car = msvcrt.getwch()
        if car in ("\x00", "\xe0"):
            return TOUCHES_SPECIALES.get(msvcrt.getwch(), "")
        if car == "\r":
            return "ENTREE"
        if car == "\x1b":
            return "ECHAP"
        if car == "\x08":
            return "EFFACER"
        if car == "\x03":
            raise KeyboardInterrupt
        return car

else:
    import select
    import termios
    import tty

    SEQUENCES = {"[A": "HAUT", "[B": "BAS", "[D": "GAUCHE", "[C": "DROITE", "[3~": "EFFACER"}
    """Sous Linux et macOS, une flèche envoie Échap ('\\x1b') suivi de
    quelques caractères, par exemple '[A' pour la flèche du haut."""

    def lire_touche():
        """Attend qu'une touche soit pressée et renvoie son nom (version Linux/macOS).

        Le terminal est passé un court instant en mode « brut » (raw) pour
        recevoir la touche immédiatement, puis remis dans son état normal.

        Renvoie "HAUT", "BAS", "GAUCHE", "DROITE", "ENTREE", "ECHAP" ou
        "EFFACER" pour les touches spéciales, sinon le caractère tapé ("5", "q"...).
        """
        fd = sys.stdin.fileno()
        ancien = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            car = os.read(fd, 1).decode(errors="ignore")
            if car == "\x1b":
                # Échap seul, ou début d'une flèche ? On lit la suite si elle arrive vite.
                suite = ""
                while select.select([fd], [], [], 0.03)[0]:
                    suite += os.read(fd, 1).decode(errors="ignore")
                return SEQUENCES.get(suite, "ECHAP" if not suite else "")
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, ancien)

        if car in ("\r", "\n"):
            return "ENTREE"
        if car in ("\x7f", "\x08"):
            return "EFFACER"
        if car == "\x03":                      # Ctrl+C en mode brut
            raise KeyboardInterrupt
        return car


def style_case(grille, fixes, erreurs, curseur, l, c):
    """Choisit la couleur d'une case pour l'affichage.

    Ordre de priorité :
      - rouge     : la case a été signalée fausse par la vérification ;
      - jaune     : même chiffre que celui sous le curseur (aide à repérer) ;
      - gras      : chiffre de départ (non modifiable) ;
      - cyan      : chiffre posé par le joueur.
    La case sous le curseur est en plus affichée en couleurs inversées.

    Renvoie la chaîne de codes ANSI à placer devant le chiffre.
    """
    v = grille[l][c]
    lc, cc = curseur

    if (l, c) in erreurs:
        style = ROUGE + GRAS
    elif v and v == grille[lc][cc]:
        style = JAUNE + GRAS
    elif (l, c) in fixes:
        style = GRAS
    else:
        style = CYAN

    if (l, c) == curseur:
        style += INVERSE
    return style


def afficher(grille, fixes, erreurs, curseur, message="", couleur=""):
    """Dessine tout l'écran : la grille, l'aide à droite et un message en bas.

    Paramètres :
        grille  : la grille à afficher.
        fixes   : ensemble des cases de départ (affichées en gras).
        erreurs : ensemble des cases à afficher en rouge.
        curseur : case (l, c) où se trouve le joueur.
        message : texte affiché sous la grille (facultatif).
        couleur : code ANSI de couleur pour ce message (facultatif).

    Tout l'écran est construit dans une liste de lignes, puis écrit en une
    seule fois. Comme on réécrit par-dessus l'ancien écran au lieu de
    l'effacer, l'affichage ne clignote pas.
    """
    lignes = [GRAS + "  S U D O K U" + RESET, "", "  " + BORD]

    for l in range(TAILLE):
        morceaux = ["|"]
        for c in range(TAILLE):
            v = grille[l][c]
            texte = str(v) if v else "."
            morceaux.append(style_case(grille, fixes, erreurs, curseur, l, c) + texte + RESET)
            if c in (2, 5):
                morceaux.append("|")          # séparateur vertical entre les blocs
        morceaux.append("|")
        lignes.append("  " + " ".join(morceaux))
        if l in (2, 5):
            lignes.append("  " + BORD)        # séparateur horizontal entre les blocs
    lignes.append("  " + BORD)

    # Ajoute l'aide et le nombre de cases vides à droite de la grille
    infos = AIDE + ["", f"Cases vides : {len(cases_vides(grille))}"]
    for i, texte in enumerate(infos):
        lignes[3 + i] += "    " + texte

    lignes += ["", "  " + couleur + message + RESET]

    # "\033[K" efface la fin de chaque ligne (restes de l'affichage précédent)
    sys.stdout.write(EN_HAUT + "\n".join(ligne + "\033[K" for ligne in lignes) + EFFACER_FIN)
    sys.stdout.flush()


def choisir_difficulte():
    """Affiche le menu de difficulté et laisse le joueur choisir.

    Flèches haut/bas pour changer de choix, Entrée pour valider.
    Renvoie le nombre de chiffres de départ correspondant (voir DIFFICULTES),
    ou None si le joueur quitte avec q ou Échap.
    """
    choix = list(DIFFICULTES)
    index = 1  # "moyen" est sélectionné par défaut
    while True:
        lignes = [GRAS + "  S U D O K U" + RESET, "",
                  "  Choisis la difficulté (flèches + Entrée) :", ""]
        for i, nom in enumerate(choix):
            texte = f" {nom.capitalize():<10} "
            lignes.append("    " + (INVERSE + texte + RESET if i == index else texte))
        sys.stdout.write(EN_HAUT + "\n".join(lignes) + EFFACER_FIN)
        sys.stdout.flush()

        touche = lire_touche()
        if touche == "HAUT":
            index = (index - 1) % len(choix)
        elif touche == "BAS":
            index = (index + 1) % len(choix)
        elif touche == "ENTREE":
            return DIFFICULTES[choix[index]]
        elif touche in ("q", "ECHAP"):
            return None


# ===========================================================================
# PARTIE 3 : la boucle de jeu
# ===========================================================================

DEPLACEMENTS = {"HAUT": (-1, 0), "BAS": (1, 0), "GAUCHE": (0, -1), "DROITE": (0, 1)}
"""Pour chaque flèche : de combien bouger le curseur, en (lignes, colonnes)."""


def jouer():
    """Déroule une partie complète.

    1. Le joueur choisit la difficulté.
    2. Le programme génère la grille et sa solution.
    3. Boucle : afficher l'écran → lire une touche → agir en conséquence.
       La boucle s'arrête quand la grille est résolue ou que le joueur quitte.

    Variables importantes :
        grille  : l'état actuel de la grille, que le joueur remplit.
        fixes   : les cases de départ, que le joueur ne peut pas modifier.
        erreurs : les cases à montrer en rouge après une vérification (touche v).
        curseur : la case où se trouve le joueur, (ligne, colonne).
    """
    nb_indices = choisir_difficulte()
    if nb_indices is None:
        return

    sys.stdout.write(EN_HAUT + EFFACER_ECRAN + "  Génération de la grille...")
    sys.stdout.flush()
    puzzle, solution = generer_puzzle(nb_indices)

    grille = [ligne[:] for ligne in puzzle]
    fixes = {(l, c) for l in range(TAILLE) for c in range(TAILLE) if puzzle[l][c]}
    erreurs = set()
    curseur = (0, 0)
    message, couleur = "Bonne partie !", ""

    while True:
        afficher(grille, fixes, erreurs, curseur, message, couleur)

        if grille == solution:
            afficher(grille, fixes, erreurs, curseur,
                     "Bravo, grille résolue ! (une touche pour quitter)", VERT)
            lire_touche()
            return

        touche = lire_touche()
        message, couleur = "", ""
        l, c = curseur

        # Flèches : déplacer le curseur. Le modulo % fait revenir de l'autre
        # côté quand on sort de la grille (ex. à droite de la colonne 8 → colonne 0).
        if touche in DEPLACEMENTS:
            dl, dc = DEPLACEMENTS[touche]
            curseur = ((l + dl) % TAILLE, (c + dc) % TAILLE)

        # Chiffre de 1 à 9 : le poser, seulement s'il respecte les règles.
        # Un chiffre qui respecte les règles mais n'est pas le bon est accepté :
        # c'est au joueur de s'en rendre compte (ou d'utiliser la touche v).
        elif len(touche) == 1 and touche in "123456789":
            v = int(touche)
            if (l, c) in fixes:
                message, couleur = "Case de départ : non modifiable.", ROUGE
                continue
            ancienne = grille[l][c]
            grille[l][c] = 0   # on vide la case pour ne pas tester v contre lui-même
            if Contraintes(grille).possible(l, c, v):
                grille[l][c] = v
                erreurs.discard((l, c))
            else:
                grille[l][c] = ancienne
                message, couleur = f"{v} est déjà dans la ligne, la colonne ou le bloc.", ROUGE

        # Effacer la case (sauf si c'est une case de départ)
        elif touche in ("0", " ", ".", "EFFACER"):
            if (l, c) not in fixes:
                grille[l][c] = 0
                erreurs.discard((l, c))

        # Indice : révèle la bonne valeur, sur la case du curseur si elle est vide
        elif touche == "i":
            vides = cases_vides(grille)
            if vides:
                il, ic = (l, c) if (l, c) in vides else random.choice(vides)
                grille[il][ic] = solution[il][ic]
                curseur = (il, ic)
                message, couleur = f"Indice : {solution[il][ic]} en ({il + 1}, {ic + 1})", VERT

        # Vérification : compare chaque chiffre posé à la solution
        elif touche == "v":
            erreurs = {(el, ec) for el in range(TAILLE) for ec in range(TAILLE)
                       if grille[el][ec] and grille[el][ec] != solution[el][ec]}
            if erreurs:
                message, couleur = f"{len(erreurs)} case(s) fausse(s), en rouge.", ROUGE
            else:
                message, couleur = "Aucune erreur pour l'instant.", VERT

        # Solution : l'affiche et termine la partie
        elif touche == "s":
            afficher(solution, fixes, set(), curseur,
                     "Solution affichée. (une touche pour quitter)", JAUNE)
            lire_touche()
            return

        elif touche in ("q", "ECHAP"):
            return


def main():
    """Point d'entrée du programme.

    Prépare l'écran, lance la partie, puis remet toujours la console dans
    son état normal (curseur visible, couleurs par défaut), même si le joueur
    quitte brutalement avec Ctrl+C. C'est le rôle du bloc `finally`.
    """
    sys.stdout.write(CACHER_CURSEUR + EN_HAUT + EFFACER_ECRAN)
    try:
        jouer()
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(RESET + MONTRER_CURSEUR + "\n")
        sys.stdout.flush()


# Ce bloc ne s'exécute que si on lance ce fichier directement
# (et pas si on l'importe depuis un autre fichier).
if __name__ == "__main__":
    main()