import matplotlib.pyplot as plt
import numpy as np

def afficher_image(img, titre="Chemin", sauvegarde=None):
    plt.figure(figsize=(10, 10))
    plt.imshow(img, interpolation="nearest")
    plt.title(titre)
    plt.axis("off")
    if sauvegarde:
        plt.savefig(sauvegarde, bbox_inches="tight")
    plt.show()