# -*- coding: utf-8 -*-
"""
Created on Tue May 30 16:28:41 2023

@author: skrzypczak
"""

from PIL import Image, ImageDraw

# Dimensions de la grille
grid_width = 800
grid_height = 600
size = 40  # Taille d'une case de la grille

# Couleurs des cases de la grille
color1 = "#D0DEA1"  # Couleur 1
color2 = "#F6E78F"  # Couleur 2


# Création de l'image
image = Image.new('RGB', (grid_width, grid_height), color=color1)
draw = ImageDraw.Draw(image)

# Remplissage de la grille avec les deux couleurs
for x in range(0, grid_width, size):
    for y in range(0, grid_height, size):
        if (x // size) % 2 == (y // size) % 2:
            draw.rectangle([(x, y), (x + size, y + size)], fill=color2)

# Dessin des contours en bas et à gauche
draw.line([(0, grid_height - 1), (grid_width, grid_height - 1)], fill='black', width=1)  # Contour bas
draw.line([(grid_width - 1, 0), (grid_width - 1, grid_height)], fill='black', width=1)  # Contour gauche
draw.line([(0, grid_height - 1), (grid_width, grid_height - 1)], fill='black', width=1)  # Contour bas
draw.line([(grid_width - 1, 0), (grid_width - 1, grid_height)], fill='black', width=1)  # Contour gauche
# Sauvegarde de l'image
image_path = './assets/grid.png'
image.save(image_path)


coordinates = []
for x in range(size // 2, grid_width, size):
    for y in range(size // 2, grid_height, size):
        coordinates.append((x, y))

# Affichage des coordonnées
for coord in coordinates:
    print(coord)