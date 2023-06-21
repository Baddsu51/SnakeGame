from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# Créer une nouvelle image avec un fond transparent
size = (80, 80)  # Modifier la taille du carré
image = Image.new("RGBA", size, (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Définir les coordonnées du carré avec des bords arrondis
x1, y1 = 0, 0
x2, y2 = size[0] - 1, size[1] - 1
radius = 30 # Modifier le rayon des bords arrondis

# Ajuster les coordonnées pour que le carré atteigne les bords de l'image
x2 -= 1
y2 -= 1

# Définir la couleur de remplissage verte
green = '#779226'

# Dessiner un carré avec des bords arrondis et la nouvelle couleur
draw.rectangle([(x1 + radius, y1), (x2 - radius, y2)], fill=green)
draw.rectangle([(x1, y1 + radius), (x2, y2 - radius)], fill=green)
draw.pieslice([(x1, y1), (x1 + radius * 2, y1 + radius * 2)], 180, 270, fill=green)
draw.pieslice([(x2 - radius * 2, y1), (x2, y1 + radius * 2)], 270, 360, fill=green)
draw.pieslice([(x1, y2 - radius * 2), (x1 + radius * 2, y2)], 90, 180, fill=green)
draw.pieslice([(x2 - radius * 2, y2 - radius * 2), (x2, y2)], 0, 90, fill=green)


# Enregistrer l'image
image.save("./assets/carre_arrondi.png")

# Charger l'image
image = Image.open("./assets/carre_arrondi.png")

# Afficher l'image
plt.imshow(image)
plt.axis('off')  # Supprimer les axes
plt.show()