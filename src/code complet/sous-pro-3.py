
# ==========================================================
# SOUS-PROJET 3 — Algorithme génétique (version simple)
# ==========================================================

###############################Q1################################################
def dans_grille(w, h, c):
    """Vérifie si la cellule c est dans la grille w*h."""
    x, y = c
    return 0 <= x < w and 0 <= y < h

def est_libre(M, c):
    """Vérifie si la cellule c est libre """
    x, y = c
    return M[y, x] == 1

def dist_manhattan(a, b):
    """Distance de Manhattan (heuristique simple) entre deux points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


###############################Q2################################################

def simuler(M, depart, but, prog, pher=None, seuil=5.0):
    """
    Simule l'exécution d'un programme (individu) dans le labyrinthe.

    Entrées :
       M : labyrinthe en numpy array (0 mur, 1 libre)
      depart, but : (x,y)
      prog : liste d'entiers (0..7) = directions
      pher : matrice de phéromones ,pher empêche l’algorithme génétique
      de refaire toujoursles mêmes chemins ratés.
      seuil : seuil au-dessus duquel on considère une "collision" phéromones

    Sortie :
      fin : position finale (x,y)
      chemin : liste des positions visitées
      collision : True si on tape un mur / sort de la grille / zone très phéromonée
      atteint : True si but atteint
    """
    h, w = M.shape
    pos = depart
    chemin = [pos]

    for d in prog:
        dx, dy = DIRECTIONS[d]
        nxt = (pos[0] + dx, pos[1] + dy)

        # collision : hors-grille ou mur
        if not dans_grille(w, h, nxt) or not est_libre(M, nxt):
            return pos, chemin, True, False

        # collision "phéromone" : on évite les zones trop marquées (optionnel)
        if pher is not None and pher[nxt[1], nxt[0]] >= seuil:
            return pos, chemin, True, False

        pos = nxt
        chemin.append(pos)

        if pos == but:
            return pos, chemin, False, True

    return pos, chemin, False, (pos == but)


###############################Q3################################################
def fitness(M, depart, but, prog, pher=None, seuil=5.0):
    """
    Calcule la fitness (score à minimiser).

    Idée :
      On veut se rapprocher du but (distance Manhattan faible).
      On pénalise les collisions (mur / hors-grille).
      On pénalise les boucles (repasser sur les mêmes cases).
      On pénalise les gènes "inutiles" (si la simu s'arrête avant la fin).
      Bonus si on avance (chemin long sans collision) et gros bonus si but atteint.
      Option) phéromones : légère pénalité/bonus pour guider la recherche.

    Sortie :
      score (float) : plus petit = meilleur( 'est moi)
      chemin : chemin simulé
      atteint (bool)
      collision (bool)
    """
    fin, chemin, collision, atteint = simuler(M, depart, but, prog, pher, seuil=seuil)

    score = dist_manhattan(fin, but)

    if collision:
        score += 80

    # pénalités simples
    score += 0.3 * (len(chemin) - len(set(chemin)))         # boucles
    score += 0.2 * (len(prog) - (len(chemin) - 1))          # gènes inutiles
    score -= 0.5 * (len(chemin) - 1)                        # bonus avance

    # phéromones (faible) : on ajoute un petit coût cumulé
    if pher is not None:
        for (x, y) in chemin:
            score += 0.05 * min(pher[y, x], 10)

    if atteint:
        score -= 200

    return score, chemin, atteint, collision


###############################Q4################################################
def case_plus_loin(carte_distances):
    """
    Choisit la case la plus loin du but (distance maximale) comme départ.
    Ça permet souvent de rendre le problème plus intéressant.
    """
    h = len(carte_distances)
    w = len(carte_distances[0])

    meilleure_case = None
    meilleure_distance = -1

    for y in range(h):
        for x in range(w):
            v = carte_distances[y][x]
            if isinstance(v, int) and v >= 0 and v > meilleure_distance:
                meilleure_distance = v
                meilleure_case = (x, y)

    return meilleure_case

def creer_population(N, L):
    """ Crée une population de N individus, chacun de longueur L (directions 0..7)."""
    return [[rd.randint(0, 7) for i in range(L)] for k in range(N)]

def selection(pop, scores, taux=0.3):
    """
    Sélection des meilleurs individus.
    On trie par score (plus petit = meilleur)
    On garde k = taux * N individus
    """
    k = max(1, int(len(pop) * taux))
    idx = np.argsort(scores)
    return [pop[i] for i in idx[:k]]

def croisement(p1, p2):
    """
    Croisement 1 point.
    On coupe entre 1/3 et 2/3 pour éviter des coupes extrêmes.
    """
    cut = rd.randint(len(p1)//3, 2*len(p1)//3)
    return p1[:cut] + p2[cut:]

def mutation(pop, taux=0.15):
    """
    On change aléatoirement quelques gènes dans la population.
    Remarque : ici le calcul de nb mutations est volontairement modéré
    pour éviter une mutation trop agressive.
    """
    N, L = len(pop), len(pop[0])
    nb = max(1, int(N * L * taux / 10))
    for i  in range(nb):
        i = rd.randint(0, N - 1)
        j = rd.randint(0, L - 1)
        pop[i][j] = rd.randint(0, 7)

###############################Q5################################################
def creer_pheromones(lab):
    """
    Crée et initialise une matrice de phéromones.

    La matrice a exactement la même taille que le labyrinthe.
    Chaque case contient une valeur flottante initialisée à 0.
    """
    hauteur = len(lab)
    largeur = len(lab[0])

    pheromones = np.zeros((hauteur, largeur), dtype=float)
    return pheromones


def deposer_pheromones(pher, chemin, depot=0.3):
    """
    Dépose des phéromones sur un chemin.

    Principe :
    - On renforce uniquement les dernières cases du chemin.
    - Cela permet de marquer les zones problématiques (collisions).
    """
    nb_cases = 10  # nombre de cases renforcées

    for i in range(min(nb_cases, len(chemin))):
        x, y = chemin[-1 - i]
        pher[y, x] += depot


###############################Q6################################################

def algorithme_genetique_simple(lab, depart, but,
                               N=80, L=150, generations=200,
                               taux_selection=0.3, taux_mutation=0.15,
                               activer_pheromones=True,
                               debut_pheromones=80,
                               depot=0.3,
                               evaporation=0.05,
                               seuil_mur=5.0):
    """
    Objectif :
      Trouver un programme (suite de directions 0..7) qui amène du départ au but.

    Paramètres à étudier :
     N : taille population
     L : longueur individus
     taux_selection (TS)
     taux_mutation (TM)

    Sortie :
     meilleur_chemin : chemin (liste de positions) du meilleur individu trouvé
                         (même si le but n'est pas atteint)
     loss : liste de la meilleure fitness par génération
    """
    M = np.array(lab, dtype=np.uint8)
    pher = creer_pheromones(lab) if activer_pheromones else None

    pop = creer_population(N, L)
    loss = []

    # on garde le meilleur sur TOUTES les générations (meilleur global) ---
    best_global_score = float("inf")
    best_global_chemin = None
    best_global_ok = False
    best_global_gen = -1

    for g in range(generations):
        scores = []
        infos = []

        # phéromones activées seulement après un certain nombre de générations
        use_pher = (pher is not None and g >= debut_pheromones)

        # évaluation de la population
        for prog in pop:
            s, chemin, atteint, collision = fitness(
                M, depart, but, prog,
                pher if use_pher else None,
                seuil=seuil_mur
            )
            scores.append(s)
            infos.append((chemin, atteint, collision))

        #  meilleur de la génération
        best_i = int(np.argmin(scores))
        best_s = scores[best_i]
        best_chemin, best_ok, best_coll = infos[best_i]
        loss.append(best_s)

        # ça garantit qu'on peut sauvegarder un "meilleur parcours GA"
        if best_s < best_global_score:
            best_global_score = best_s
            best_global_chemin = best_chemin
            best_global_ok = best_ok
            best_global_gen = g

        #  stop si but atteint
        if best_ok:
            print("Solution trouvée génération", g, "| fitness =", round(best_s, 2))
            return best_chemin, loss

        # phéromones : évaporation + dépôt sur chemins de collision
        if use_pher:
            pher *= (1.0 - evaporation)
            for (chemin, ok, coll) in infos:
                if coll and not ok:
                    deposer_pheromones(pher, chemin, depot=depot)

        # nouvelle génération : sélection -> croisement -> mutation
        surv = selection(pop, scores, taux_selection)

        enfants = []
        while len(enfants) < N - len(surv):
            p1 = rd.choice(surv)
            p2 = rd.choice(surv)
            enfants.append(croisement(p1, p2))

        pop = surv + enfants
        mutation(pop, taux_mutation)

    # on renvoie quand même le meilleur global ---
    # C'est exactement ce qu'il faut pour : "sauvegarder l'image du parcours sélectionné"
    print("GA terminé sans atteindre le but.",
          "| meilleur fitness =", round(best_global_score, 2),
          "| gen =", best_global_gen,
          "| atteint =", best_global_ok)

    return best_global_chemin, loss

# ==========================================================
# TESTS SP3 — 
# ==========================================================

print("TEST SP3 ")


# On fixe un labyrinthe "référence

N_lab = 40
graine_lab = 7
lab = generer_labyrinthe(N_lab, N_lab, graine=graine_lab)

# But aléatoire mais libre

but = case_libre_aleatoire(lab)

# Départ = case la plus loin (à partir de la carte BFS)

carte = construire_carte_distances(lab, but)
depart = case_plus_loin(carte)

print("Lab =", N_lab, "x", N_lab, "| graine =", graine_lab)


print("Depart =", depart, "| But =", but, "| dist_BFS(depart) =", carte[depart[1]][depart[0]])



# Référence : chemin optimal BFS (pour comparer)

dirs_bfs = construire_carte_directions(carte)
chemin_bfs = reconstruire_chemin(dirs_bfs, depart)

if chemin_bfs is None:
    print("BFS : pas de chemin")
    longueur_bfs = None
else:
    longueur_bfs = len(chemin_bfs) - 1
    print("BFS : chemin trouvé | longueur =", longueur_bfs)

    img_bfs = image_chemin(lab, chemin_bfs, depart=depart, but=but)
    afficher_image(img_bfs, titre=" Référence BFS", sauvegarde="reference_bfs.png")
    print("Image sauvegardée : reference_bfs.png")



# Run GA 
#    -> ce test sert à montrer : la fitness baisse (même si but pas atteint)

print("TEST A : GA baseline (avec phéromones) ")

chemin_ga, loss = algorithme_genetique_simple(
    lab, depart, but,
    N=80, L=150, generations=200,
    taux_selection=0.30, taux_mutation=0.15,
    activer_pheromones=True
)

# Courbe fitness 
plt.figure()
plt.plot(loss)
plt.title("Fitness (GA baseline)")
plt.xlabel("Générations")
plt.ylabel("Fitness (plus bas = meilleur)")
plt.grid(True)
plt.savefig("fitness_baseline.png", bbox_inches="tight", pad_inches=0)
plt.show()

print("Fitness début =", round(loss[0], 2), "| fin =", round(loss[-1], 2), "| min =", round(min(loss), 2))

# Image du meilleur chemin GA (même si but pas atteint)
if chemin_ga is None:
    print("GA : aucun chemin renvoyé (rare si tu renvoies best_global_chemin).")
else:
    print("GA : chemin renvoyé | longueur =", len(chemin_ga) - 1, "| fin =", chemin_ga[-1])
    img_ga = image_chemin(lab, chemin_ga, depart=depart, but=but)
    afficher_image(img_ga, titre="GA baseline", sauvegarde="parcours_ga_baseline.png")
    print("Image sauvegardée : parcours_ga_baseline.png")


# -----------------------------
#  Comparaison SIMPLE : avec vs sans phéromones
#   test pour le rapport (“effet des phéromones”)
# -----------------------------
print(" TEST B : GA avec vs sans phéromones ")

configs_pher = [
    ("SANS pher", False),
    ("AVEC pher", True),
]

for nom, activer in configs_pher:
    chemin_tmp, loss_tmp = algorithme_genetique_simple(
        lab, depart, but,
        N=80, L=150, generations=150,
        taux_selection=0.30, taux_mutation=0.15,
        activer_pheromones=activer
    )
    print(nom, "| fitness_fin =", round(loss_tmp[-1], 2), "| min =", round(min(loss_tmp), 2),
          "| chemin_recu =", (chemin_tmp is not None))

    # mini-courbe 
    plt.figure()
    plt.plot(loss_tmp)
    plt.title(f"Fitness {nom}")
    plt.xlabel("Générations")
    plt.ylabel("Fitness")
    plt.grid(True)
    plt.savefig(f"fitness_{nom.replace(' ', '_')}.png", bbox_inches="tight", pad_inches=0)
    plt.show()
    print("Courbe sauvegardée :", f"fitness_{nom.replace(' ', '_')}.png")


# -----------------------------
# Étude paramètres ultra simple et lisible (3 variantes)
# -----------------------------
print("TEST C : Variations paramètres (3 cas)")
tests_params = [
    # (nom, N, L, TS, TM)
    ("Plus petit", 60, 100, 0.30, 0.15),
    ("Baseline",   80, 150, 0.30, 0.15),
    ("Plus grand", 120, 200, 0.30, 0.15),
]

for nom, Np, Lp, TS, TM in tests_params:
    chemin_tmp, loss_tmp = algorithme_genetique_simple(
        lab, depart, but,
        N=Np, L=Lp, generations=150,
        taux_selection=TS, taux_mutation=TM,
        activer_pheromones=False  # pour comparer proprement (moins de bruit)
    )

    print(f"{nom:10s} | N={Np:3d} L={Lp:3d} TS={TS} TM={TM} | fin={round(loss_tmp[-1],2)} | min={round(min(loss_tmp),2)}")

print("FIN de projet (finalement)")

print("C'était Fun , merci beaucoup ")


