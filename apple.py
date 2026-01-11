"""
Classe Apple - Gestion de la pomme dans le jeu Snake
"""

import turtle
from random import choice
from typing import List, Tuple

from PIL import Image

from config import (
    APPLE_IMAGE,
    APPLE_SIZE,
    TEMP_APPLE_GIF,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    CELL_SIZE,
)


class Apple:
    """
    Représente la pomme que le serpent doit manger.
    """

    def __init__(self, screen: turtle.Screen):
        """
        Initialise la pomme.
        
        Args:
            screen: L'écran Turtle sur lequel afficher la pomme.
        """
        self._screen = screen
        self._coordinates = self._generate_grid_coordinates()
        
        # Charger et préparer l'image de la pomme
        self._prepare_apple_image()
        
        # Créer la tortue pour la pomme
        self._turtle = turtle.Turtle()
        self._turtle.shape(TEMP_APPLE_GIF)
        self._turtle.shapesize(60, 60)
        self._turtle.color("red")
        self._turtle.penup()
        self._turtle.speed(0)
        
        # Position initiale
        self.spawn([])

    def _generate_grid_coordinates(self) -> List[Tuple[int, int]]:
        """
        Génère la liste de toutes les coordonnées valides de la grille.
        
        Returns:
            Liste de tuples (x, y) représentant les positions valides.
        """
        coordinates = []
        real_height = WINDOW_HEIGHT // 2
        real_width = WINDOW_WIDTH // 2
        
        for x in range(CELL_SIZE // 2, WINDOW_WIDTH, CELL_SIZE):
            for y in range(CELL_SIZE // 2, WINDOW_HEIGHT, CELL_SIZE):
                coordinates.append((x - real_width, y - real_height))
        
        return coordinates

    def _prepare_apple_image(self):
        """Charge l'image de la pomme et la convertit en GIF."""
        try:
            image = Image.open(APPLE_IMAGE)
            image.thumbnail(APPLE_SIZE)
            image.save(TEMP_APPLE_GIF)
            self._screen.register_shape(TEMP_APPLE_GIF)
        except Exception as e:
            print(f"Avertissement: Impossible de charger l'image de la pomme - {e}")
            # Utiliser une forme par défaut
            self._screen.register_shape("circle")

    def spawn(self, forbidden_positions: List[Tuple[float, float]]):
        """
        Place la pomme à une nouvelle position aléatoire.
        
        Args:
            forbidden_positions: Liste des positions occupées par le serpent.
        """
        # Trouver une position valide
        available_positions = [
            pos for pos in self._coordinates 
            if pos not in forbidden_positions
        ]
        
        if available_positions:
            x, y = choice(available_positions)
        else:
            # Fallback si toutes les positions sont occupées
            x, y = choice(self._coordinates)
        
        self._turtle.goto(x, y)

    def get_position(self) -> Tuple[float, float]:
        """
        Retourne la position actuelle de la pomme.
        
        Returns:
            Tuple (x, y) de la position.
        """
        return self._turtle.position()

    def distance_to(self, position: Tuple[float, float]) -> float:
        """
        Calcule la distance entre la pomme et une position donnée.
        
        Args:
            position: Position (x, y) à comparer.
            
        Returns:
            Distance en pixels.
        """
        return self._turtle.distance(position)

    def is_eaten(self, head_position: Tuple[float, float], threshold: float = 35) -> bool:
        """
        Vérifie si la pomme a été mangée par le serpent.
        
        Args:
            head_position: Position de la tête du serpent.
            threshold: Distance minimale pour considérer la pomme comme mangée.
            
        Returns:
            True si la pomme est mangée, False sinon.
        """
        return self.distance_to(head_position) <= threshold

    def cleanup(self):
        """Nettoie les ressources de la pomme."""
        try:
            self._turtle.hideturtle()
            self._turtle.clear()
        except turtle.TurtleGraphicsError:
            pass
