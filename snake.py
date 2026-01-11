"""
Classe Snake - Gestion du serpent dans le jeu
"""

import turtle
from typing import List, Tuple

from PIL import Image

from config import (
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
)


class Snake:
    """
    Représente le serpent contrôlé par le joueur.
    """

    def __init__(self, screen: turtle.Screen):
        """
        Initialise le serpent.
        
        Args:
            screen: L'écran Turtle sur lequel afficher le serpent.
        """
        self._screen = screen
        self._direction = DIRECTION_STOP
        self._body: List[turtle.Turtle] = []
        self._positions: List[Tuple[float, float]] = []
        self._length = 0
        
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
            
        except Exception as e:
            print(f"Avertissement: Impossible de charger l'image de la tête - {e}")
        
        try:
            # Image du corps
            body_image = Image.open(BODY_IMAGE)
            body_image.thumbnail(IMAGE_SIZE)
            body_image.save(TEMP_BODY_GIF)
            self._screen.register_shape(TEMP_BODY_GIF)
            
        except Exception as e:
            print(f"Avertissement: Impossible de charger l'image du corps - {e}")

    def move(self):
        """Déplace le serpent dans la direction actuelle."""
        speed = 4
        
        if self._direction == DIRECTION_UP:
            self._head.shape(TEMP_HEAD_SOUTH_GIF)
            self._head.setheading(90)
            self._head.speed(speed)
            self._head.forward(CELL_SIZE)
            
        elif self._direction == DIRECTION_DOWN:
            self._head.shape(TEMP_HEAD_NORTH_GIF)
            self._head.setheading(270)
            self._head.speed(speed)
            self._head.forward(CELL_SIZE)
            
        elif self._direction == DIRECTION_LEFT:
            self._head.shape(TEMP_HEAD_EAST_GIF)
            self._head.setheading(180)
            self._head.speed(speed)
            self._head.forward(CELL_SIZE)
            
        elif self._direction == DIRECTION_RIGHT:
            self._head.shape(TEMP_HEAD_WEST_GIF)
            self._head.setheading(0)
            self._head.speed(speed)
            self._head.forward(CELL_SIZE)
        
        # Enregistrer la nouvelle position
        self._positions.append(self._head.position())
        
        # Déplacer le corps
        if self._length > 0:
            x, y = self._positions[-2]
            self._body[-1].goto(x, y)
            self._body.insert(0, self._body.pop())
        
        # Nettoyer les anciennes positions
        if len(self._positions) > self._length + 1:
            del self._positions[:-self._length - 1]

    def set_direction(self, direction: str):
        """
        Change la direction du serpent.
        Empêche le demi-tour (aller dans la direction opposée).
        
        Args:
            direction: Nouvelle direction (Up, Down, Left, Right).
        """
        if self._direction != OPPOSITE_DIRECTIONS.get(direction):
            self._direction = direction

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
        
        # Repositionner la tête
        self._head.goto(SNAKE_START_X, SNAKE_START_Y)
        self._head.shape(TEMP_HEAD_NORTH_GIF)
        self._positions.append(self._head.position())

    def cleanup(self):
        """Nettoie toutes les ressources du serpent."""
        try:
            self._head.hideturtle()
            self._head.clear()
            for segment in self._body:
                segment.hideturtle()
                segment.clear()
        except turtle.TurtleGraphicsError:
            pass
