"""
Configuration du jeu Snake - Constantes et chemins des ressources
"""

import os
import sys
import tempfile


def resource_path(relative_path: str) -> str:
    """
    Obtient le chemin absolu vers une ressource.
    Fonctionne pour le développement et pour PyInstaller.
    """
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Dimensions de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Snake Game"

# Taille des cases de la grille
CELL_SIZE = 40

# Vitesse du jeu (délai entre chaque frame en secondes)
GAME_SPEED = 0.17

# Limites du terrain de jeu
BOUNDARY_X = 390
BOUNDARY_Y = 290

# Position initiale du serpent
SNAKE_START_X = -20
SNAKE_START_Y = 0

# Couleurs
BACKGROUND_COLOR = "black"
SNAKE_BODY_COLOR = "#779226"
SCORE_COLOR = "black"

# Taille des images
IMAGE_SIZE = (40, 40)
APPLE_SIZE = (35, 35)

# Dossier temporaire pour les images GIF converties
TEMP_DIR = tempfile.gettempdir()

# Chemins des assets
ASSETS_DIR = resource_path("./assets")

# Images
APPLE_IMAGE = resource_path("./assets/apple.png")
BODY_IMAGE = resource_path("./assets/carre_arrondi.png")
HEAD_IMAGE = resource_path("./assets/head_snake.png")
GRID_IMAGE = resource_path("./assets/grid.png")

# Sons
SOUND_EAT = resource_path("./assets/apple_munch_noice.wav")
SOUND_HIT = resource_path("./assets/punch_whistle_noice.wav")

# Fichier de score
SCORE_FILE = resource_path("./assets/score.txt")

# Chemins des fichiers temporaires pour les images GIF
TEMP_APPLE_GIF = os.path.join(TEMP_DIR, "snake_temp_apple.gif")
TEMP_BODY_GIF = os.path.join(TEMP_DIR, "snake_temp_body.gif")
TEMP_HEAD_NORTH_GIF = os.path.join(TEMP_DIR, "snake_temp_head_north.gif")
TEMP_HEAD_SOUTH_GIF = os.path.join(TEMP_DIR, "snake_temp_head_south.gif")
TEMP_HEAD_EAST_GIF = os.path.join(TEMP_DIR, "snake_temp_head_east.gif")
TEMP_HEAD_WEST_GIF = os.path.join(TEMP_DIR, "snake_temp_head_west.gif")

# Contrôles clavier (ZQSD pour clavier AZERTY français)
KEY_UP = "z"
KEY_DOWN = "s"
KEY_LEFT = "q"
KEY_RIGHT = "d"
KEY_PAUSE = "Escape"
KEY_QUIT = "x"

# Directions
DIRECTION_UP = "Up"
DIRECTION_DOWN = "Down"
DIRECTION_LEFT = "Left"
DIRECTION_RIGHT = "Right"
DIRECTION_STOP = "Stop"

# Opposés des directions (pour empêcher le demi-tour)
OPPOSITE_DIRECTIONS = {
    DIRECTION_UP: DIRECTION_DOWN,
    DIRECTION_DOWN: DIRECTION_UP,
    DIRECTION_LEFT: DIRECTION_RIGHT,
    DIRECTION_RIGHT: DIRECTION_LEFT,
}
