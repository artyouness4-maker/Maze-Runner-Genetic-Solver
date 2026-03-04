# ################################################################
# ####################sous_projet_2###############################
# ################################################################


############################Q1###############################################

def construire_carte_distances(labyrinthe, but):
    """
    Construit une carte des distances minimales vers le but.

    Principe :
    Tous les déplacements ont le même coût (1).
    Le problème revient donc à un BFS (équivalent à Dijkstra ici).
    On démarre du but et on propage les distances vers l'extérieur.

    Entrées :
      labyrinthe : 
            0 -> mur
            1 -> case libre
      but : couple (x, y)

    Sortie :
      distances[y][x] :
            -1   : mur
            None : case libre mais non atteignable
            0..  : distance minimale jusqu'au but
    """
    hauteur = len(labyrinthe)
    largeur = len(labyrinthe[0])
    bx, by = but

    # Initialisation de la matrice des distances
    # Par défaut : None (case libre non encore atteinte)
    distances = [[None for i in range(largeur)] for k in range(hauteur)]

    # Marquage des murs
    # On met -1 pour distinguer clairement les murs
    for y in range(hauteur):
        for x in range(largeur):
            if labyrinthe[y][x] == 0:
                distances[y][x] = -1

    # Sécurité , si le but est hors de la grille
    if not (0 <= bx < largeur and 0 <= by < hauteur):
        return distances

    # Si le but est sur un mur, aucune propagation possible
    if labyrinthe[by][bx] == 0:
        return distances

    # Initialisation du BFS :
    # le but est à distance 0
    distances[by][bx] = 0
    file = deque([(bx, by)])

    # BFS classique
    while file:
        x, y = file.popleft()
        d = distances[y][x]

        # Exploration des 8 voisins
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy

            # Vérification des limites de la grille
            if 0 <= nx < largeur and 0 <= ny < hauteur:

                # On ne propage que sur des cases libres non encore visitées
                if labyrinthe[ny][nx] == 1 and distances[ny][nx] is None:
                    distances[ny][nx] = d + 1
                    file.append((nx, ny))

    return distances



# ==========================================================
# TESTS -
# ==========================================================

# print("TEST : construire_carte_distances (BFS) : ")

# lab = generer_labyrinthe(20, 20, graine=0)
# but = (3, 0) #si on le change on va tout changer   bien sûr
# dist = construire_carte_distances(lab, but)

# print(" ")

# print(dist )

# print(" ")
###########################Q2###############################################

def construire_carte_directions(distances):
    """
    Construit une carte directionnelle à partir de la carte des distances.

    méthodes :
    Chaque case connaît sa distance minimale au but.
    On choisit, pour chaque case, un voisin dont la distance est strictement plus petite.
    En suivant ces directions, on "descend" vers le but.

    Entrée :
      distances[y][x] :
            -1   : mur
            None : non atteignable
            int : distance au but

    Sortie :
      directions[y][x] :
            None    : mur ou non atteignable
            "GOAL"  : case du but
            d (0..7): direction à suivre pour se rapprocher du but
    """
    hauteur = len(distances)
    largeur = len(distances[0])

    # Initialisation de la carte directionnelle
    directions = [[None for i in range(largeur)] for j in range(hauteur)]

    for y in range(hauteur):
        for x in range(largeur):
            val = distances[y][x]

            # Mur ou cases non atteignables
            if val is None or val == -1:
                continue

            # Cas particulier : le but
            if val == 0:
                directions[y][x] = "GOAL"
                continue

            # Recherche du voisin avec distance strictement plus petite
            meilleure_dir = None
            meilleure_val = val

            for d, (dx, dy) in enumerate(DIRECTIONS):
                nx, ny = x + dx, y + dy

                if 0 <= nx < largeur and 0 <= ny < hauteur:
                    v = distances[ny][nx]

                    # On accepte uniquement les voisins valides(comme des étudiants)
                    # dont la distance est plus petite
                    if isinstance(v, int) and v >= 0 and v < meilleure_val:
                        meilleure_val = v
                        meilleure_dir = d

            # Direction chosie (ou None si aucun voisin plus proche)
            directions[y][x] = meilleure_dir

    return directions

def case_libre_aleatoire(lab):
    
    #la focntion donne une case libre pour les tests et on va l'utiliser aprés aussi 
    
    h, l = len(lab), len(lab[0])
    
    libres = [(x,y) for y in range(h) for x in range(l) if lab[y][x] == 1]
    
    return rd.choice(libres)


# ==========================================================
# TESTS -
# ==========================================================

#

# print(" construire_carte_directions")

# lab = generer_labyrinthe(30, 30, graine=0)

# # choisir un BUT qui est libre 

# but = case_libre_aleatoire(lab)

# dist = construire_carte_distances(lab, but)

# dirs = construire_carte_directions(dist)

# print("But =", but, "| dist(but) =", dist[but[1]][but[0]], "| dir(but) =", dirs[but[1]][but[0]])



#############################Q3##################################################
def reconstruire_chemin(directions, depart, limite=100000):
    """
     Reconstruire un chemin en suivant la carte directionnelle.

    Idée :
    directions[y][x] indique la "meilleure direction" pour se rapprocher du but
      (descente de la distance).
    En partant de depart, on suit ces directions jusqu'à tomber sur "GOAL".

    Entrées :
      directions[y][x] :
          "GOAL" si la case est le but
          None  si mur / non atteignable / pas de direction
          d (0..7) sinon : index de direction dans DIRECTIONS
      depart : tuple (x, y)
      limite : limite de sécurité pour éviter toute boucle infinie

    Sortie :
      chemin : liste [(x,y), ...] si on atteint le but
      None si bloqué / non atteignable
    """
    x, y = depart
    chemin = []

    for k in range(limite):
        chemin.append((x, y))
        d = directions[y][x]

        if d == "GOAL":
            return chemin
        if d is None:
            return None

        dx, dy = DIRECTIONS[d]
        x, y = x + dx, y + dy

    return None  # sécurité



###################################Q4##########################################
def afficher_carte_distances(distances, titre="Carte des distances ", sauvegarde=None):
    """
    Affiche la matrice des distances avec une colorbar (visualisation).
    Option : sauvegarder l'image si 'sauvegarde' est fourni.

    Entrées :
      distances : matrice issue de construire_carte_distances (Q1)
      titre : titre de la figure
      sauvegarde : soit le nom de fichier pour sauvegarder ou None pour rien
    """
    plt.figure()
    plt.title(titre)
    plt.matshow(distances, fignum=0)
    plt.colorbar()

    if sauvegarde:
        plt.savefig(sauvegarde, bbox_inches="tight", pad_inches=0)

    plt.show()

###################################Q5#########################################
    
def image_chemin(labyrinthe, chemin, depart=None, but=None):
    """
    image RGB :
      murs : noir
      libres : blanc
      chemin : rouge
      départ : bleu
      but : vert

    Entrées :
      labyrinthe : matrice 0/1
      chemin : liste [(x,y), ...] ou None
      depart : (x,y) / None
      but : (x,y) o/ None

    Sortie :
      img : tableau numpy (H, W, 3) 
    """
    h = len(labyrinthe)
    l = len(labyrinthe[0])
    img = np.zeros((h, l, 3), dtype=np.uint8)

    # Base : murs / libres
    for y in range(h):
        for x in range(l):
            img[y, x] = (255, 255, 255) if labyrinthe[y][x] == 1 else (0, 0, 0)

    # Chemin
    if chemin is not None:
        for (x, y) in chemin:
            img[y, x] = (255, 0, 0)  # rouge

    # Départ
    if depart is not None:
        x, y = depart
        img[y, x] = (0, 0, 255)    # bleu

    # But
    if but is not None:
        x, y = but
        img[y, x] = (0, 255, 0)    # vert( c'est ma couleur préferée)

    return img


def afficher_image(img, titre="Chemin", sauvegarde=None):
    """
    Affiche une image RGB et la sauvegarde si demandé.

    """
    plt.figure()
    plt.imshow(img, interpolation="nearest")
    plt.title(titre)
    plt.axis("off")

    if sauvegarde:
        plt.savefig(sauvegarde, bbox_inches="tight", pad_inches=0)

    plt.show()

# # ==========================================================
# # TESTS-
# # ==========================================================
# #Bloc A — Test “visualisation distances” (Q4)
# print("Bloc-A")

# print(" ")

# print(" TEST  Q4 : affichage carte des distances ")

# print(" ")

# # On réutilise le même labyrinthe et le même but

# print("But =", but, "| distance au but =", dist[but[1]][but[0]])

# # Affichage + sauvegarde :
# afficher_carte_distances(dist,
#     titre="Carte des distances",
#     sauvegarde="carte_distances.png"
# )


# #Bloc B — Test “pipeline complet” (Q1→Q5)
# print("Bloc-B")

# print(" TEST  chemin + distances ")

# #lab test : 
    
# lab = generer_labyrinthe(30, 30, graine=2)

# # Choix aléatoire :
    
# but = case_libre_aleatoire(lab)
# depart = case_libre_aleatoire(lab)


# dist = construire_carte_distances(lab, but)
# dirs = construire_carte_directions(dist)
# chemin = reconstruire_chemin(dirs, depart)

# print(" ")

# print(" Depart:", depart, "| But:", but)

# print(" ")

# print(" Distance depart -> but :", dist[depart[1]][depart[0]])


# print(" ")

# # Vérification simple
# if chemin is None:
#     print(" Chemin: None (départ non atteignable) ")
# else:
#     print(" Chemin trouvé | longueur =", len(chemin) - 1, "| fin =", chemin[-1])

# # Visualisation + sauvegarde
# img = image_chemin(lab, chemin, depart=depart, but=but)
# afficher_image(img, titre=" Chemin reconstruit", sauvegarde="chemin_bfs.png")


# # ==========================================================
# # Bloc C — Test d’analyse 
# #  Moyenne de longueur de solution pour N =(j'ai pas le symbole inclus) 
# # {8,16,32,64,128,256,512}
# # Idée :
# #  Pour chaque taille N, on génère plusieurs labyrinthes 
# #  On choisit un but libre, puis un départ "loin" (distance maximale)
# #  On reconstruit le chemin BFS 
# #  On mesure sa longueur (nombre de pas) et on fait la moyenne
# # ==========================================================

# #cette fonction n'était pas demander ici mais je vais l'utiliser pour le test 
# #elle  donne la case la plus loin 

# print("Bloc-C")

# def case_plus_loin(carte_distances):
#     """
#     Choisit la case la plus loin du but (distance maximale) comme départ.
#     Ça permet souvent de rendre le problème plus intéressant.
#     """
#     h = len(carte_distances)
#     w = len(carte_distances[0])

#     meilleure_case = None
#     meilleure_distance = -1

#     for y in range(h):
#         for x in range(w):
#             v = carte_distances[y][x]
#             if isinstance(v, int) and v >= 0 and v > meilleure_distance:
#                 meilleure_distance = v
#                 meilleure_case = (x, y)

#     return meilleure_case
# print("jeu de test fun : moyenne longueur solution vs N (fight) ")

# tailles = [8, 16, 32, 64, 128, 256, 512]
# nb_tests = 10

# for N in tailles:
#     longueurs = []
#     t0 = time.time()

#     for k in range(nb_tests):
#         lab = generer_labyrinthe(N, N, graine=k)  # graine pour reproductibilité
#         but = case_libre_aleatoire(lab)

#         dist = construire_carte_distances(lab, but)
#         depart = case_plus_loin(dist)

#         dirs = construire_carte_directions(dist)
#         chemin = reconstruire_chemin(dirs, depart)

#         if chemin is not None:
#             longueurs.append(len(chemin) - 1)  # nb de pas
#         else:
#             # Rare : si pas atteignable, on ignore le test(au cas ou)
#             pass

#     t1 = time.time()

#     if len(longueurs) == 0:
#         print(f"N={N:3d} | aucune solution trouvée (rare)")
#     else:
#         moyenne = sum(longueurs) / len(longueurs)
#         print(f"N={N:3d} | moy_len={moyenne:.2f} | tests_validé={len(longueurs)}/{nb_tests} | temps={t1-t0:.2f}s")


# #Bloc D — Test de validation (chemin correct ou pas)

# print("Bloc-D")
# #test directe si notre chemin est valide ou pas 
# def chemin_valide(lab, chemin, depart, but):
#     if chemin is None:
#         return False
#     if chemin[0] != depart or chemin[-1] != but:
#         return False

#     for (x, y) in chemin:
#         if lab[y][x] != 1:
#             return False

#     for i in range(len(chemin) - 1):
#         x1, y1 = chemin[i]
#         x2, y2 = chemin[i + 1]
#         if (x2 - x1, y2 - y1) not in DIRECTIONS:
#             return False

#     return True


# print("TEST  Q3 : validité du chemin reconstruit")

# lab = generer_labyrinthe(30, 30, graine=2)

# but = case_libre_aleatoire(lab)

# dist = construire_carte_distances(lab, but)

# depart = case_plus_loin(dist)

# dirs = construire_carte_directions(dist)

# chemin = reconstruire_chemin(dirs, depart)

# print("Depart:", depart, "But:", but)

# print("Chemin valide ?", chemin_valide(lab, chemin, depart, but))

