import random as rd
import numpy as np

DIRECTIONS = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]

def generer_labyrinthe(largeur, hauteur, graine=None):
    if graine is not None: rd.seed(graine)
    lab = [[0 for _ in range(largeur)] for _ in range(hauteur)]
    x, y = rd.randint(0, largeur - 1), rd.randint(0, hauteur - 1)
    lab[y][x] = 1
    pile = [(x, y)]
    while pile:
        cx, cy = pile[-1]
        candidats = []
        for dx, dy in DIRECTIONS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < largeur and 0 <= ny < hauteur and lab[ny][nx] == 0:
                voisins_1 = sum(1 for dx2, dy2 in DIRECTIONS if 0 <= nx+dx2 < largeur and 0 <= ny+dy2 < hauteur and lab[ny+dy2][nx+dx2] == 1)
                if voisins_1 == 1: candidats.append((nx, ny))
        if not candidats: pile.pop()
        else:
            nx, ny = rd.choice(candidats)
            lab[ny][nx] = 1
            pile.append((nx, ny))
    return lab