"""
Classe Game - Classe principale orchestrant le jeu Snake
"""

import turtle

from src.config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    BACKGROUND_COLOR,
    GRID_IMAGE,  # Chemin de l'image de fond
    KEY_UP,
    KEY_DOWN,
    KEY_LEFT,
    KEY_RIGHT,
    KEY_PAUSE,
    KEY_QUIT,
    KEY_REPLAY,
    DIRECTION_UP,
    DIRECTION_DOWN,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    SPEED_INITIAL,
    SPEED_MIN,
    SPEED_DECREASE_PER_POINT,
)  # imports des constantes de configuration

from src.entities.snake import Snake  # classe Snake
from src.entities.apple import Apple  # classe Apple
from src.managers.score_manager import ScoreManager  # gestionnaire de score
from src.managers.sound_manager import SoundManager  # gestionnaire de son
from src.managers.animations import AnimationManager  # gestionnaire d'animations


class Game:
    """
    Classe principale qui gère le jeu Snake.
    Orchestre tous les composants : serpent, pomme, score, sons et animations.

    Méthodes publiques:
        run: Lance le jeu.
    """

    def __init__(self):
        """Initialise le jeu et tous ses composants."""
        self._running = False
        self._paused = False
        self._game_over = False
        self._countdown_active = False  # Indique si le compte à rebours est actif
        self._current_speed = SPEED_INITIAL
        self._game_loop_id = 0  # ID pour identifier la boucle de jeu active

        self._screen = self._setup_screen()  # Initialiser l'écran

        # Initialiser les composants
        self._sound_manager = SoundManager()
        self._score_manager = ScoreManager()
        self._snake = Snake(self._screen)
        self._apple = Apple(self._screen)
        self._animation_manager = AnimationManager(self._screen)

        # Affichage de la pause
        self._pause_display = self._create_pause_display()

        # Affichage des contrôles
        self._controls_display = self._create_controls_display()

        # Configurer les contrôles
        self._setup_controls()

    def _setup_screen(self) -> turtle._Screen:
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
            print(
                f"Avertissement: Impossible de charger l'image de fond - {e}")

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
        pause_turtle.color("white")
        pause_turtle.penup()
        pause_turtle.hideturtle()
        pause_turtle.goto(1000, 1000)  # Hors écran
        return pause_turtle

    def _write_with_outline(self, writer: turtle.Turtle, text: str, x: float, y: float,
                            color: str, font: tuple, align: str = "center"):
        """
        Écrit du texte avec un contour noir pour meilleure visibilité.

        Args:
            writer: Turtle utilisée pour écrire.
            text: Texte à afficher.
            x: Position X.
            y: Position Y.
            color: Couleur du texte.
            font: Tuple (nom, taille, style) pour la police.
            align: Alignement du texte.
        """
        # Dessiner le contour noir (8 directions)
        writer.color("black")
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    writer.goto(x + dx, y + dy)
                    writer.write(text, align=align, font=font)

        # Dessiner le texte en couleur par-dessus
        writer.color(color)
        writer.goto(x, y)
        writer.write(text, align=align, font=font)

    def _create_controls_display(self) -> turtle.Turtle:
        """
        Crée l'affichage pour les instructions des contrôles.

        Returns:
            Objet Turtle pour afficher les contrôles.
        """
        controls_turtle = turtle.Turtle()
        controls_turtle.speed(0)
        controls_turtle.color("white")
        controls_turtle.penup()
        controls_turtle.hideturtle()
        controls_turtle.goto(0, -270)
        return controls_turtle

    def _show_controls(self):
        """Affiche les instructions des contrôles à l'écran."""
        self._controls_display.clear()

        # Contour noir plus subtil (1 pixel au lieu de 2)
        text = "ZQSD : Déplacer | ESC : Pause | X : Quitter | ESPACE : Rejouer"
        font = ("Arial", 12, "normal")

        self._controls_display.color("black")
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    self._controls_display.goto(0 + dx, -270 + dy)
                    self._controls_display.write(
                        text, align="center", font=font)

        # Texte en couleur par-dessus
        self._controls_display.color("#90CAF9")
        self._controls_display.goto(0, -270)
        self._controls_display.write(text, align="center", font=font)

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

        # Rejouer
        self._screen.onkey(self._handle_replay, KEY_REPLAY)

        # Gestion de la fermeture de fenêtre
        try:
            self._screen.getcanvas().winfo_toplevel().protocol(
                "WM_DELETE_WINDOW",
                self._quit_game
            )
        except Exception:
            pass

    def _go_up(self):
        """Change la direction vers le haut."""
        if not self._game_over and not self._countdown_active:
            self._snake.set_direction(DIRECTION_UP)

    def _go_down(self):
        """Change la direction vers le bas."""
        if not self._game_over and not self._countdown_active:
            self._snake.set_direction(DIRECTION_DOWN)

    def _go_left(self):
        """Change la direction vers la gauche."""
        if not self._game_over and not self._countdown_active:
            self._snake.set_direction(DIRECTION_LEFT)

    def _go_right(self):
        """Change la direction vers la droite."""
        if not self._game_over and not self._countdown_active:
            self._snake.set_direction(DIRECTION_RIGHT)

    def _toggle_pause(self):
        """Active ou désactive la pause."""
        if self._game_over or self._countdown_active:
            return

        self._paused = not self._paused

        if self._paused:
            self._apple.stop_animation()
            self._pause_display.clear()
            self._write_with_outline(
                self._pause_display, "PAUSE", 0, -40,
                "white", ("Arial", 80, "bold")
            )
        else:
            self._apple.start_animation()
            self._pause_display.clear()
            self._pause_display.goto(1000, 1000)

    def _handle_replay(self):
        """Gère l'appui sur ESPACE pour rejouer."""
        if self._game_over:
            self._restart_game()

    def _quit_game(self):
        """Quitte le jeu proprement."""
        self._running = False

    def _calculate_speed(self) -> int:
        """
        Calcule la vitesse actuelle en fonction du score.

        Returns:
            Délai en millisecondes entre chaque mouvement.
        """
        score = self._score_manager.score
        speed_seconds = max(SPEED_MIN, SPEED_INITIAL -
                            (score * SPEED_DECREASE_PER_POINT))
        return int(speed_seconds * 1000)

    def _start_countdown(self):
        """Lance le compte à rebours avant le début du jeu."""
        self._countdown_active = True
        self._screen.update()
        self._animation_manager.show_countdown(self._on_countdown_complete)

    def _on_countdown_complete(self):
        """Appelé quand le compte à rebours est terminé."""
        self._countdown_active = False
        # Démarrer le serpent automatiquement vers la droite
        self._snake.set_direction(DIRECTION_RIGHT)
        # Incrémenter l'ID pour invalider les anciennes boucles
        self._game_loop_id += 1
        self._game_loop(self._game_loop_id)

    def _show_game_over(self):
        """Affiche l'écran Game Over."""
        self._game_over = True
        self._apple.stop_animation()

        # Cacher la trainée
        self._snake.hide_trail()
        self._animation_manager.hide_trail()

        # Animation de mort
        body_turtles = self._snake.get_body_turtles()
        self._snake.hide_head()

        def on_death_complete():
            self._animation_manager.show_game_over(
                self._score_manager.score,
                self._score_manager.highscore,
                self._restart_game
            )
            self._screen.update()

        if body_turtles:
            self._animation_manager.animate_death(
                body_turtles, on_death_complete)
        else:
            on_death_complete()

    def _restart_game(self):
        """Redémarre le jeu après Game Over."""
        self._game_over = False
        self._animation_manager.hide_game_over()

        # Réinitialiser
        self._score_manager.reset()
        self._snake.reset()
        self._apple.spawn(self._snake.get_all_positions())
        self._apple.start_animation()
        self._current_speed = SPEED_INITIAL

        # Mettre à jour l'écran
        self._screen.update()

        # Relancer le compte à rebours
        self._start_countdown()

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
        head_pos = self._snake.get_head_position()
        if self._apple.is_eaten(head_pos):
            self._sound_manager.play_eat()
            self._score_manager.add_point()
            self._snake.grow()

            # Animation de manger
            x, y = head_pos
            self._animation_manager.animate_eat(x, y)
            self._apple.flash_eaten()

            # Nouvelle position pour la pomme
            self._apple.spawn(self._snake.get_all_positions())

    def _game_loop(self, loop_id: int):
        """
        Boucle principale du jeu utilisant ontimer pour la fluidité.

        Args:
            loop_id: ID de cette boucle pour éviter les boucles multiples.
        """
        # Vérifier si cette boucle est encore valide
        if loop_id != self._game_loop_id or not self._running:
            return

        if self._game_over or self._countdown_active:
            # Ne pas continuer la boucle pendant game over ou countdown
            return

        if not self._paused:
            # Déplacer le serpent
            self._snake.move()

            # Vérifier les collisions
            if self._check_collisions():
                self._show_game_over()
                self._screen.update()
                return

            # Vérifier si la pomme est mangée
            self._check_apple_eaten()

            # Mettre à jour l'écran
            self._screen.update()

            # Calculer le délai en fonction du score
            delay = self._calculate_speed()
            self._screen.ontimer(lambda: self._game_loop(loop_id), delay)
        else:
            # En pause, juste mettre à jour l'écran
            self._screen.update()
            self._screen.ontimer(lambda: self._game_loop(loop_id), 100)

    def run(self):
        """Lance le jeu."""
        print("=== Snake Game ===")
        print(
            f"Controles: {KEY_UP.upper()}/{KEY_DOWN.upper()}/{KEY_LEFT.upper()}/{KEY_RIGHT.upper()} pour se deplacer")
        print(f"Pause: {KEY_PAUSE}")
        print(f"Quitter: {KEY_QUIT.upper()}")
        print(f"Rejouer: ESPACE")
        print("==================")

        self._running = True

        # Afficher les contrôles à l'écran une seule fois
        self._show_controls()

        try:
            # Lancer le compte à rebours puis le jeu
            self._start_countdown()

            # Maintenir la fenêtre ouverte
            self._screen.mainloop()
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

        self._running = False

        # Sauvegarder le score
        self._score_manager.save_highscore()

        # Nettoyer les composants
        try:
            self._sound_manager.cleanup()
            self._score_manager.cleanup()
            self._snake.cleanup()
            self._apple.cleanup()
            self._animation_manager.cleanup()
        except Exception:
            pass

        print("Au revoir!")
