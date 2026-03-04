import numpy as np
import random as rd
from collections import deque
from .generator import DIRECTIONS

# --- BFS / DIJKSTRA ---
def construire_carte_distances(labyrinthe, but):
    h, w = len(labyrinthe), len(labyrinthe[0])
    bx, by = but
    distances = [[-1 if labyrinthe[y][x] == 0 else None for x in range(w)] for y in range(h)]
    if distances[by][bx] == -1: return distances
    distances[by][bx] = 0
    file = deque([(bx, by)])
    while file:
        x, y = file.popleft()
        d = distances[y][x]
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and distances[ny][nx] is None:
                distances[ny][nx] = d + 1
                file.append((nx, ny))
    return distances

# --- ALGORITHME GÉNÉTIQUE ---
def fitness(M, depart, but, prog, pher=None, seuil=5.0):
    # (Insère ici ta fonction simuler et fitness complète que tu as écrite)
    # C'est la partie la plus "IA" de ton CV !
    pass