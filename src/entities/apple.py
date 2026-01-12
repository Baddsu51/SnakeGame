"""
Classe Apple - Gestion de la pomme dans le jeu Snake
"""

import turtle
from random import choice
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from turtle import _Screen

from PIL import Image

from src.config import (
    APPLE_IMAGE,
    APPLE_SIZE,
    TEMP_APPLE_GIF,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    CELL_SIZE,
    APPLE_PULSE_MIN,
    APPLE_PULSE_MAX,
    APPLE_PULSE_SPEED,
)


class Apple:
    """
    Représente la pomme que le serpent doit manger.
    Inclut des animations de pulsation.

    Méthodes publiques:
        - spawn(forbidden_positions: List[Tuple[float, float]]): Place la pomme à une nouvelle position aléatoire
        - get_position() -> Tuple[float, float]: Retourne la position actuelle de la pomme
        - distance_to(position: Tuple[float, float]) -> float: Calcule la distance entre la pomme et une position
        - is_eaten(head_position: Tuple[float, float], threshold: float = 35) -> bool: Vérifie si la pomme a été mangée
        - stop_animation(): Arrête l'animation de la pomme
        - start_animation(): Reprend l'animation de la pomme
        - flash_eaten(): Effet visuel quand la pomme est mangée
        - cleanup(): Nettoie les ressources de la pomme
    """

    def __init__(self, screen: "_Screen"):
        """
        Initialise la pomme.

        Args:
            screen: L'écran Turtle sur lequel afficher la pomme.
        """
        self._screen = screen
        self._coordinates = self._generate_grid_coordinates()

        # Animation de pulsation
        self._pulse_scale = 1.0
        self._pulse_growing = True
        self._animating = True

        self._prepare_apple_image()  # Charger et préparer l'image de la pomme

        # Créer la tortue pour la pomme
        self._turtle = turtle.Turtle()
        self._turtle.shape(TEMP_APPLE_GIF)
        self._turtle.shapesize(1, 1)
        self._turtle.color("red")
        self._turtle.penup()
        self._turtle.speed(0)

        # Position initiale
        self.spawn([])

        # Démarrer l'animation de pulsation
        self._start_pulse_animation()

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
        except (FileNotFoundError, OSError, IOError) as e:
            print(
                f"Avertissement: Impossible de charger l'image de la pomme - {e}")
            # Utiliser une forme par défaut
            self._screen.register_shape("circle")

    def spawn(self, forbidden_positions: List[Tuple[float, float]]):
        """
        Place la pomme à une nouvelle position aléatoire.

        Args:
            forbidden_positions: Liste des positions occupées par le serpent.
        """
        # Trouver une position valide
        # Exclure la zone du score en haut à gauche (x < -300 et y > 200)
        available_positions = [
            pos for pos in self._coordinates
            if pos not in forbidden_positions
            and not (pos[0] < -300 and pos[1] > 200)
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

    def _start_pulse_animation(self):
        """Démarre l'animation de pulsation de la pomme."""
        self._animate_pulse()

    def _animate_pulse(self):
        """
        Animation de pulsation continue de la pomme.
        La pomme grossit et rétrécit légèrement.
        """
        if not self._animating:
            return

        # Calculer le nouveau facteur d'échelle
        pulse_step = 0.02

        if self._pulse_growing:
            self._pulse_scale += pulse_step
            if self._pulse_scale >= APPLE_PULSE_MAX:
                self._pulse_growing = False
        else:
            self._pulse_scale -= pulse_step
            if self._pulse_scale <= APPLE_PULSE_MIN:
                self._pulse_growing = True

        # Appliquer l'échelle
        try:
            self._turtle.shapesize(self._pulse_scale, self._pulse_scale)
        except turtle.TurtleGraphicsError:
            return

        # Continuer l'animation
        try:
            self._screen.ontimer(self._animate_pulse, APPLE_PULSE_SPEED)
        except (turtle.TurtleGraphicsError, RuntimeError):
            pass

    def stop_animation(self):
        """Arrête l'animation de la pomme."""
        self._animating = False

    def start_animation(self):
        """Reprend l'animation de la pomme."""
        if not self._animating:
            self._animating = True
            self._start_pulse_animation()

    def flash_eaten(self):
        """
        Effet visuel quand la pomme est mangée.
        Flash rapide avant de respawn.
        """
        # Sauvegarder la position actuelle
        current_pos = self._turtle.position()

        # Effet de grossissement rapide
        try:
            self._turtle.shapesize(1.5, 1.5)
            self._screen.update()
        except turtle.TurtleGraphicsError:
            pass

    def cleanup(self):
        """Nettoie les ressources de la pomme."""
        self._animating = False
        try:
            self._turtle.hideturtle()
            self._turtle.clear()
        except (turtle.TurtleGraphicsError, Exception):
            # Ignorer toutes les erreurs liées à la destruction de la fenêtre
            pass
