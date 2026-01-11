"""
Classe Game - Classe principale orchestrant le jeu Snake
"""

import time
import turtle

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    BACKGROUND_COLOR,
    GRID_IMAGE,
    GAME_SPEED,
    KEY_UP,
    KEY_DOWN,
    KEY_LEFT,
    KEY_RIGHT,
    KEY_PAUSE,
    KEY_QUIT,
    DIRECTION_UP,
    DIRECTION_DOWN,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
)
from snake import Snake
from apple import Apple
from score_manager import ScoreManager
from sound_manager import SoundManager


class Game:
    """
    Classe principale qui gère le jeu Snake.
    Orchestre tous les composants : serpent, pomme, score et sons.
    """

    def __init__(self):
        """Initialise le jeu et tous ses composants."""
        self._running = False
        self._paused = False
        
        # Initialiser l'écran
        self._screen = self._setup_screen()
        
        # Initialiser les composants
        self._sound_manager = SoundManager()
        self._score_manager = ScoreManager()
        self._snake = Snake(self._screen)
        self._apple = Apple(self._screen)
        
        # Affichage de la pause
        self._pause_display = self._create_pause_display()
        
        # Configurer les contrôles
        self._setup_controls()

    def _setup_screen(self) -> turtle.Screen:
        """
        Configure et retourne l'écran de jeu.
        
        Returns:
            L'objet Screen configuré.
        """
        screen = turtle.Screen()
        screen.title(WINDOW_TITLE)
        screen.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        screen.bgcolor(BACKGROUND_COLOR)
        
        # Charger l'image de fond
        try:
            screen.bgpic(GRID_IMAGE)
        except turtle.TurtleGraphicsError as e:
            print(f"Avertissement: Impossible de charger l'image de fond - {e}")
        
        screen.tracer(0)
        return screen

    def _create_pause_display(self) -> turtle.Turtle:
        """
        Crée l'affichage pour le texte de pause.
        
        Returns:
            Objet Turtle pour afficher "Pause".
        """
        pause_turtle = turtle.Turtle()
        pause_turtle.speed(0)
        pause_turtle.color("black")
        pause_turtle.penup()
        pause_turtle.hideturtle()
        pause_turtle.goto(1000, 1000)  # Hors écran
        return pause_turtle

    def _setup_controls(self):
        """Configure les contrôles clavier."""
        self._screen.listen()
        
        # Contrôles de direction (ZQSD)
        self._screen.onkeypress(self._go_up, KEY_UP)
        self._screen.onkeypress(self._go_down, KEY_DOWN)
        self._screen.onkeypress(self._go_left, KEY_LEFT)
        self._screen.onkeypress(self._go_right, KEY_RIGHT)
        
        # Pause et quitter
        self._screen.onkey(self._toggle_pause, KEY_PAUSE)
        self._screen.onkey(self._quit_game, KEY_QUIT)
        
        # Gestion de la fermeture de fenêtre
        self._screen.getcanvas().winfo_toplevel().protocol(
            "WM_DELETE_WINDOW", 
            self._quit_game
        )

    def _go_up(self):
        """Change la direction vers le haut."""
        self._snake.set_direction(DIRECTION_UP)

    def _go_down(self):
        """Change la direction vers le bas."""
        self._snake.set_direction(DIRECTION_DOWN)

    def _go_left(self):
        """Change la direction vers la gauche."""
        self._snake.set_direction(DIRECTION_LEFT)

    def _go_right(self):
        """Change la direction vers la droite."""
        self._snake.set_direction(DIRECTION_RIGHT)

    def _toggle_pause(self):
        """Active ou désactive la pause."""
        self._paused = not self._paused
        
        if self._paused:
            self._pause_display.goto(0, -40)
            self._pause_display.write(
                "Pause",
                align="center",
                font=("Arial", 120, "bold")
            )
        else:
            self._pause_display.clear()
            self._pause_display.goto(1000, 1000)

    def _quit_game(self):
        """Quitte le jeu proprement."""
        self._running = False

    def _reset(self):
        """Réinitialise le jeu après une collision."""
        self._score_manager.reset()
        self._snake.reset()
        self._apple.spawn(self._snake.get_all_positions())

    def _check_collisions(self) -> bool:
        """
        Vérifie toutes les collisions.
        
        Returns:
            True si une collision a eu lieu, False sinon.
        """
        # Collision avec les murs
        if self._snake.check_wall_collision():
            self._sound_manager.play_hit()
            return True
        
        # Collision avec soi-même
        if self._snake.check_self_collision():
            self._sound_manager.play_hit()
            return True
        
        return False

    def _check_apple_eaten(self):
        """Vérifie si la pomme a été mangée et gère la croissance."""
        if self._apple.is_eaten(self._snake.get_head_position()):
            self._sound_manager.play_eat()
            self._score_manager.add_point()
            self._snake.grow()
            self._apple.spawn(self._snake.get_all_positions())

    def _game_loop(self):
        """Boucle principale du jeu."""
        while self._running:
            if not self._paused:
                self._screen.update()
                
                # Déplacer le serpent
                self._snake.move()
                
                # Vérifier les collisions
                if self._check_collisions():
                    self._reset()
                    continue
                
                # Vérifier si la pomme est mangée
                self._check_apple_eaten()
                
                # Délai pour contrôler la vitesse
                time.sleep(GAME_SPEED)
            else:
                # Même en pause, mettre à jour l'écran
                self._screen.update()
                time.sleep(0.1)

    def run(self):
        """Lance le jeu."""
        print("=== Snake Game ===")
        print(f"Contrôles: {KEY_UP.upper()}/{KEY_DOWN.upper()}/{KEY_LEFT.upper()}/{KEY_RIGHT.upper()} pour se déplacer")
        print(f"Pause: {KEY_PAUSE}")
        print(f"Quitter: {KEY_QUIT.upper()}")
        print("==================")
        
        self._running = True
        
        try:
            self._game_loop()
        except turtle.Terminator:
            # La fenêtre a été fermée
            pass
        except KeyboardInterrupt:
            # Ctrl+C
            pass
        finally:
            self._cleanup()

    def _cleanup(self):
        """Nettoie toutes les ressources."""
        print("\nFermeture du jeu...")
        
        # Sauvegarder le score
        self._score_manager.save_highscore()
        
        # Nettoyer les composants
        self._sound_manager.cleanup()
        self._score_manager.cleanup()
        self._snake.cleanup()
        self._apple.cleanup()
        
        # Fermer la fenêtre Turtle
        try:
            self._screen.bye()
        except turtle.Terminator:
            pass
        
        print("Au revoir!")
