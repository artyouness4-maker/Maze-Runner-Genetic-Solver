Maze Runner : Étude Algorithmique et Résolution Évolutive
Ce projet académique porte sur la génération procédurale de structures labyrinthiques et l'implémentation de solveurs utilisant des approches déterministes et stochastiques. L'objectif est de comparer l'efficacité des algorithmes classiques de recherche de chemin avec des méthodes d'optimisation par intelligence artificielle.

Architecture Technique
Le projet est structuré autour de trois piliers fondamentaux :

1. Génération Procédurale (Depth-First Search)
Algorithme : Utilisation du parcours en profondeur (DFS) avec une variante aléatoire pour la création de labyrinthes arborescents parfaits.

Mécanisme : Implémentation via une structure de données en pile (stack) pour supporter le processus de backtracking.

Contrainte de connectivité : Application stricte de la règle de voisinage à 8 directions pour garantir l'absence de cycles et de zones isolées.

Scalabilité : Algorithme optimisé pour la génération de matrices haute résolution (jusqu'à 500x500 unités).

2. Analyse et Résolution Déterministe (Dijkstra)
Calcul de Distance : Implémentation de l'algorithme de Dijkstra pour générer une carte de distances euclidiennes précises vers la cible (Goal).

Extraction de Chemin : Création d'un champ de vecteurs directionnels permettant la reconstruction instantanée du chemin optimal à partir de n'importe quel point de départ libre.

Visualisation : Exploitation de Matplotlib pour le rendu de heatmaps de distance et l'analyse de la topologie du labyrinthe.

3. Résolution par Algorithme Génétique
Le projet explore un paradigme d'IA inspiré de la théorie de l'évolution pour résoudre des labyrinthes sans connaissance préalable de leur structure globale :

Représentation Génomique : Les chemins sont encodés sous forme de vecteurs de directions (0 à 7).

Processus Évolutif : Application itérative de la sélection de survie, du croisement (crossover) et de la mutation aléatoire.

Fonction de Fitness : Évaluation multicritère basée sur la distance de Manhattan au but, avec des pénalités pour les collisions et les boucles.

Optimisation de Convergence : Intégration d'un système de dépôt de phéromones pour identifier les impasses et optimiser l'exploration des générations futures.