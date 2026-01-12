"""
Classe Snake - Gestion du serpent dans le jeu
"""

import turtle
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from turtle import _Screen

from PIL import Image

from src.config import (
    HEAD_IMAGE,
    BODY_IMAGE,
    IMAGE_SIZE,
    TEMP_HEAD_NORTH_GIF,
    TEMP_HEAD_SOUTH_GIF,
    TEMP_HEAD_EAST_GIF,
    TEMP_HEAD_WEST_GIF,
    TEMP_BODY_GIF,
    SNAKE_START_X,
    SNAKE_START_Y,
    SNAKE_BODY_COLOR,
    CELL_SIZE,
    BOUNDARY_X,
    BOUNDARY_Y,
    DIRECTION_UP,
    DIRECTION_DOWN,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_STOP,
    OPPOSITE_DIRECTIONS,
    TRAIL_LENGTH,
    TRAIL_COLORS,
)


class Snake:
    """
    Représente le serpent contrôlé par le joueur.
    Inclut des animations fluides et une trainée visuelle.

    Méthodes publiques:
        - move(): Déplace le serpent dans la direction actuelle avec animation fluide
        - hide_trail(): Cache la trainée du serpent
        - set_direction(direction: str): Change la direction du serpent (empêche les demi-tours)
        - grow(): Ajoute un segment au corps du serpent
        - check_wall_collision() -> bool: Vérifie si le serpent touche les bords
        - check_self_collision() -> bool: Vérifie si le serpent se mord la queue
        - get_head_position() -> Tuple[float, float]: Retourne la position de la tête
        - get_all_positions() -> List[Tuple[float, float]]: Retourne toutes les positions occupées
        - is_moving (propriété): Retourne True si le serpent est en mouvement
        - reset(): Réinitialise le serpent à son état initial
        - get_body_turtles() -> List[turtle.Turtle]: Retourne la liste des turtles du corps
        - hide_head(): Cache la tête du serpent
        - show_head(): Affiche la tête du serpent
        - cleanup(): Nettoie toutes les ressources du serpent
    """

    def __init__(self, screen: "_Screen"):
        """
        Initialise le serpent.

        Args:
            screen: L'écran Turtle sur lequel afficher le serpent.
        """
        self._screen = screen
        self._direction = DIRECTION_STOP
        # Pour éviter les changements multiples par frame
        self._next_direction = DIRECTION_STOP
        self._body: List[turtle.Turtle] = []  # Segments du corps
        # Historique des positions
        self._positions: List[Tuple[float, float]] = []
        self._length = 0  # Longueur du serpent

        self._trail_turtles: List[turtle.Turtle] = []  # Trainée visuelle
        self._init_trail()

        # Préparer les images
        self._prepare_images()

        # Créer la tête du serpent
        self._head = turtle.Turtle()
        self._head.speed(0)
        self._head.shape(TEMP_HEAD_NORTH_GIF)
        self._head.shapesize(1)
        self._head.color("black")
        self._head.penup()
        self._head.goto(SNAKE_START_X, SNAKE_START_Y)

        # Ajouter la position initiale
        self._positions.append(self._head.position())

    def _init_trail(self):
        """Initialise les turtles pour la trainée visuelle."""
        for i in range(TRAIL_LENGTH):
            t = turtle.Turtle()
            t.speed(0)
            t.shape("circle")
            # Taille décroissante
            size = max(0.3, 1.0 - (i * 0.15))
            t.shapesize(size, size)
            # Couleur de la trainée
            color_index = min(i, len(TRAIL_COLORS) - 1)
            t.color(TRAIL_COLORS[color_index])
            t.penup()
            t.hideturtle()
            self._trail_turtles.append(t)

    def _prepare_images(self):
        """Prépare toutes les images du serpent."""
        try:
            # Image de la tête
            head_image = Image.open(HEAD_IMAGE)
            head_image.thumbnail(IMAGE_SIZE)

            # Sauvegarder les rotations pour chaque direction
            head_image.save(TEMP_HEAD_NORTH_GIF)  # Nord (par défaut)

            head_south = head_image.rotate(180)
            head_south.save(TEMP_HEAD_SOUTH_GIF)

            head_east = head_image.rotate(270)
            head_east.save(TEMP_HEAD_EAST_GIF)

            head_west = head_image.rotate(90)
            head_west.save(TEMP_HEAD_WEST_GIF)

            # Enregistrer les formes
            self._screen.register_shape(TEMP_HEAD_NORTH_GIF)
            self._screen.register_shape(TEMP_HEAD_SOUTH_GIF)
            self._screen.register_shape(TEMP_HEAD_EAST_GIF)
            self._screen.register_shape(TEMP_HEAD_WEST_GIF)

        except (FileNotFoundError, OSError, IOError) as e:
            print(
                f"Avertissement: Impossible de charger l'image de la tête - {e}")

        try:
            # Image du corps
            body_image = Image.open(BODY_IMAGE)
            body_image.thumbnail(IMAGE_SIZE)
            body_image.save(TEMP_BODY_GIF)
            self._screen.register_shape(TEMP_BODY_GIF)

        except (FileNotFoundError, OSError, IOError) as e:
            print(
                f"Avertissement: Impossible de charger l'image du corps - {e}")

    def move(self):
        """Déplace le serpent dans la direction actuelle avec animation fluide."""
        # Appliquer la direction en attente
        self._direction = self._next_direction

        if self._direction == DIRECTION_STOP:
            return

        # Sauvegarder la position précédente
        prev_x, prev_y = self._head.xcor(), self._head.ycor()

        # Calculer la nouvelle position
        if self._direction == DIRECTION_UP:
            self._head.shape(TEMP_HEAD_SOUTH_GIF)
            new_x, new_y = prev_x, prev_y + CELL_SIZE

        elif self._direction == DIRECTION_DOWN:
            self._head.shape(TEMP_HEAD_NORTH_GIF)
            new_x, new_y = prev_x, prev_y - CELL_SIZE

        elif self._direction == DIRECTION_LEFT:
            self._head.shape(TEMP_HEAD_EAST_GIF)
            new_x, new_y = prev_x - CELL_SIZE, prev_y

        elif self._direction == DIRECTION_RIGHT:
            self._head.shape(TEMP_HEAD_WEST_GIF)
            new_x, new_y = prev_x + CELL_SIZE, prev_y
        else:
            return

        # Déplacer la tête directement (plus fluide)
        self._head.goto(new_x, new_y)

        # Enregistrer la nouvelle position
        self._positions.append(self._head.position())

        # Déplacer le corps
        if self._length > 0:
            x, y = self._positions[-2]
            self._body[-1].goto(x, y)
            self._body.insert(0, self._body.pop())

        # Mettre à jour la trainée
        self._update_trail()

        # Nettoyer les anciennes positions (garder plus pour la trainée)
        max_positions = max(self._length + 1, TRAIL_LENGTH + 2)
        if len(self._positions) > max_positions:
            del self._positions[:-max_positions]

    def _update_trail(self):
        """Met à jour la trainée visuelle derrière le serpent."""
        # Ne montrer la trainée que si le serpent bouge
        if self._direction == DIRECTION_STOP or len(self._positions) < 2:
            for t in self._trail_turtles:
                t.hideturtle()
            return

        # Prendre les positions pour la trainée (après le corps)
        body_end_index = -(self._length + 1) if self._length > 0 else -1
        trail_positions = self._positions[:body_end_index][-TRAIL_LENGTH:]

        for i, trail_turtle in enumerate(self._trail_turtles):
            pos_index = len(trail_positions) - 1 - i
            if pos_index >= 0 and pos_index < len(trail_positions):
                trail_turtle.goto(trail_positions[pos_index])
                trail_turtle.showturtle()
            else:
                trail_turtle.hideturtle()

    def hide_trail(self):
        """Cache la trainée du serpent."""
        for t in self._trail_turtles:
            t.hideturtle()

    def set_direction(self, direction: str):
        """
        Change la direction du serpent.
        Empêche le demi-tour (aller dans la direction opposée).

        Args:
            direction: Nouvelle direction (Up, Down, Left, Right).
        """
        # Vérifier par rapport à la direction actuelle OU la prochaine direction
        current = self._direction if self._direction != DIRECTION_STOP else self._next_direction
        if current != OPPOSITE_DIRECTIONS.get(direction):
            self._next_direction = direction

    def grow(self):
        """Ajoute un segment au corps du serpent."""
        self._length += 1

        # Créer un nouveau segment
        segment = turtle.Turtle()
        segment.speed(0)

        try:
            segment.shape(TEMP_BODY_GIF)
        except turtle.TurtleGraphicsError:
            segment.shape("square")

        segment.shapesize(CELL_SIZE // 20)
        segment.color(SNAKE_BODY_COLOR)
        segment.penup()

        # Placer le segment à la dernière position
        if len(self._positions) >= self._length:
            segment.goto(self._positions[-self._length])

        self._body.append(segment)

    def check_wall_collision(self) -> bool:
        """
        Vérifie si le serpent touche les bords.

        Returns:
            True si collision, False sinon.
        """
        x, y = self._head.xcor(), self._head.ycor()
        return (
            x > BOUNDARY_X or
            x < -BOUNDARY_X or
            y > BOUNDARY_Y or
            y < -BOUNDARY_Y
        )

    def check_self_collision(self) -> bool:
        """
        Vérifie si le serpent se mord la queue.

        Returns:
            True si collision, False sinon.
        """
        head_pos = self._head.position()
        return head_pos in self._positions[:-1]

    def get_head_position(self) -> Tuple[float, float]:
        """
        Retourne la position de la tête.

        Returns:
            Tuple (x, y) de la position de la tête.
        """
        return self._head.position()

    def get_all_positions(self) -> List[Tuple[float, float]]:
        """
        Retourne toutes les positions occupées par le serpent.

        Returns:
            Liste des positions.
        """
        return list(self._positions)

    @property
    def is_moving(self) -> bool:
        """Retourne True si le serpent est en mouvement."""
        return self._direction != DIRECTION_STOP

    def reset(self):
        """Réinitialise le serpent à son état initial."""
        # Cacher et supprimer les segments du corps
        for segment in self._body:
            segment.goto(1000, 1000)
            segment.hideturtle()

        self._body.clear()
        self._positions.clear()
        self._length = 0
        self._direction = DIRECTION_STOP
        self._next_direction = DIRECTION_STOP

        # Cacher la trainée
        self.hide_trail()

        # Repositionner la tête
        self._head.goto(SNAKE_START_X, SNAKE_START_Y)
        self._head.shape(TEMP_HEAD_NORTH_GIF)
        self._head.showturtle()
        self._positions.append(self._head.position())

    def get_body_turtles(self) -> List[turtle.Turtle]:
        """
        Retourne la liste des turtles du corps.
        Utilisé pour les animations de mort.

        Returns:
            Liste des segments du corps.
        """
        return self._body.copy()

    def hide_head(self):
        """Cache la tête du serpent."""
        self._head.hideturtle()

    def show_head(self):
        """Affiche la tête du serpent."""
        self._head.showturtle()

    def cleanup(self):
        """Nettoie toutes les ressources du serpent."""
        try:
            self._head.hideturtle()
            self._head.clear()
            for segment in self._body:
                segment.hideturtle()
                segment.clear()
            for t in self._trail_turtles:
                t.hideturtle()
        except (turtle.TurtleGraphicsError, Exception):
            # Ignorer toutes les erreurs liées à la destruction de la fenêtre
            pass
