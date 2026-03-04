from src.generator import generer_labyrinthe
from src.solvers import construire_carte_distances, algorithme_genetique_simple
from src.utils import afficher_image, image_chemin

# Exemple d'exécution
lab = generer_labyrinthe(50, 50, graine=42)
but = (0, 0)
# Lancement des calculs...
print("Labyrinthe généré, calcul du chemin en cours...")