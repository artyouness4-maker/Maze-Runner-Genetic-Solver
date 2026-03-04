import random as rd
import numpy as np
import matplotlib.pyplot as plt
import time
from collections import deque

# ------------------------------------------------------------
#    j'ai respecter le schéma de l'énoncé
#     DIRECTIONS (8 voisins) : 0 → 7
#              3  2  1
#              4  X  0
#              5  6  7
# ------------------------------------------------------------
DIRECTIONS = [
    (+1, 0),    # 0 : droite
    (+1, -1),   # 1 : haut-droite
    (0, -1),    # 2 : haut
    (-1, -1),   # 3 : haut-gauche
    (-1, 0),    # 4 : gauche
    (-1, +1),   # 5 : bas-gauche
    (0, +1),    # 6 : bas
    (+1, +1)    # 7 : bas-droite
]

################################################################
######################sous_projet_1#############################
################################################################


###########################Q1##############################################

def generer_labyrinthe(largeur, hauteur, graine=None):
    """
    Génére un labyrinth sous forme de matrice :
      0 = mur
      1 = chemin (case libre)

    Méthode :
      DFS aléatoire avec pile .
      On part d'une case choisie au hasard puis on étend le chemin.

    anti-boucle :
      Une case candidate n'est ajoutée que si elle touche exactement
      1 seule case déjà libre dans le voisinage à 8 directions.
      Cela évite les cycles et donne un labyrinthe plutôt en "couloirs".

     'graine' : c
      Fixe le générateur aléatoire => même graine => même labyrinthe.
      (seulement pour simplifier le travail pendant les tests
       et le travail dans tout le projet ")
    """
    if graine is not None:
        rd.seed(graine)

    lab = [[0 for i in range(largeur)] for j in range(hauteur)]

    # départ aléatoire
    x = rd.randint(0, largeur - 1)
    y = rd.randint(0, hauteur - 1)
    lab[y][x] = 1
    pile = [(x, y)]

    while pile:
        cx, cy = pile[-1]
        candidats = []

        for dx, dy in DIRECTIONS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < largeur and 0 <= ny < hauteur and lab[ny][nx] == 0:

                # règle anti-boucle : exactement 1 voisin déjà libre
                voisins_1 = 0
                for dx2, dy2 in DIRECTIONS:
                    vx, vy = nx + dx2, ny + dy2
                    if 0 <= vx < largeur and 0 <= vy < hauteur and lab[vy][vx] == 1:
                        voisins_1 += 1

                if voisins_1 == 1:
                    candidats.append((nx, ny))

        if not candidats:#si la liste est pas vide 
            pile.pop()  
        else:
            nx, ny = rd.choice(candidats)
            lab[ny][nx] = 1
            pile.append((nx, ny))

    return lab


# # ==========================================================
# # TESTS -
# # ==========================================================



# print(" TEST  génération du labyrinthe :  ")

# lab1 = generer_labyrinthe(30, 30, graine=10)
# lab2 = generer_labyrinthe(30, 30, graine=10)

# print(lab1)
# print(" ")

# print("teste (graine=10) :", lab1 == lab2)

# print(" ")

# # Test — temps + tailles diffèrentes 

# for N in [5,20, 50, 500,]:
#     t0 = time.time()
#     lab = generer_labyrinthe(N, N, graine=1)
#     t1 = time.time()
#     print(f"N={N:2d} | temps={t1-t0:.4f}s ")


##################################Q2###########################################

def labyrinthe_vers_rgb(lab, but=None):
    """
    Convertir un labyrinthe en image RGB :
      mur (0)   : noir
      libre (1) : blanc
      but       : rouge (s'il y en a )

    petite note :
      Si but=None, on utilise (-1,-1) pour éviter
      de colorier une case réelle par erreur
    """
    h, l = len(lab), len(lab[0])
    
    img = np.zeros((h, l, 3), dtype=np.uint8)

    bx, by = (-1, -1) if but is None else but

    for y in range(h):
        for x in range(l):
            if (x, y) == (bx, by):
                img[y, x] = (255, 0, 0)        # rouge
            elif lab[y][x] == 1:
                img[y, x] = (255, 255, 255)    # blanc
            else:
                img[y, x] = (0, 0, 0)          # noir

    return img


def afficher_labyrinthe(lab, but=None, titre="Labyrinthe", sauvegarde=None):
    """
    Affiche le labyrinthe sous forme d'image.
    Si 'sauvegarde' est renseigné, l'image est enregistrée.
    """
    img = labyrinthe_vers_rgb(lab, but)

    plt.figure()
    plt.imshow(img)
    plt.title(titre)
    plt.axis("off")

    if sauvegarde:
        plt.savefig(sauvegarde, bbox_inches="tight", pad_inches=0)

    plt.show()


# # ==========================================================
# # TESTS — 
# # ==========================================================

# for i in range(3):
#     print(" ")
#     print("Q2 :  labyrinthe ")
#     print(" ")
#     lab = generer_labyrinthe(30, 30, graine=i)

#     but = (0, 0)
#     print(" ")
#     print("but rouge en : ", but)
#     print(" ")
#     afficher_labyrinthe(lab, but=but, titre=" maze by youn ")



