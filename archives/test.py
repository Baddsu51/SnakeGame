# -*- coding: utf-8 -*-
"""
Created on Tue May 30 11:52:23 2023

@author: skrzypczak
"""

from PIL import Image

# Charger l'image
image_originale = Image.open("./assets/apple.png")


# Récupérer les dimensions de l'image originale
largeur_originale, hauteur_originale = image_originale.size

# Définir les nouvelles dimensions de l'image agrandie
facteur_agrandissement = 2
largeur_agrandie = largeur_originale * facteur_agrandissement
hauteur_agrandie = hauteur_originale * facteur_agrandissement

# Créer une nouvelle image agrandie avec les dimensions spécifiées
image_agrandie = Image.new("RGBA", (largeur_agrandie, hauteur_agrandie))

# Parcourir chaque pixel de l'image agrandie
for y in range(hauteur_originale):
    for x in range(largeur_originale):
        # Obtenir la couleur du pixel dans l'image originale
        couleur = image_originale.getpixel((x, y))

        # Obtenir le canal alpha du pixel
        alpha = couleur[3] if len(couleur) == 4 else 255

        # Définir la couleur du bloc de 4 pixels dans l'image agrandie
        x_agrandi = x * facteur_agrandissement
        y_agrandi = y * facteur_agrandissement
        for i in range(facteur_agrandissement):
            for j in range(facteur_agrandissement):
                image_agrandie.putpixel((x_agrandi + i, y_agrandi + j), (couleur[0], couleur[1], couleur[2], alpha))


# Sauvegarder l'image agrandie
image_agrandie.save("./assets/applex2.png")
