"""
Gestionnaire d'animations pour le jeu Snake
"""

import turtle
from typing import List, Tuple, Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from turtle import _Screen

from src.config import (
    POPUP_DURATION,
    POPUP_RISE_DISTANCE,
    COLOR_POPUP,
    COLOR_GAME_OVER,
    COLOR_COUNTDOWN,
    COLOR_GO,
    COLOR_REPLAY_TEXT,
    DEATH_ANIMATION_STEPS,
    DEATH_ANIMATION_DELAY,
    TRAIL_LENGTH,
    TRAIL_COLORS,
    COUNTDOWN_DELAY,
    GO_DELAY,
    ANIMATION_FRAME_MS,
)


class AnimationManager:
    """
    Gère toutes les animations du jeu Snake.
    Utilise les timers Turtle pour des animations fluides.

    Méthodes publiques:
        update_trail: Met à jour la trainée visuelle du serpent.
        hide_trail: Cache toute la trainée.
        show_score_popup: Affiche un popup animé qui monte et disparaît.
        show_countdown: Affiche le compte à rebours (3, 2, 1, GO!).
        show_game_over: Affiche l'écran Game Over.
        hide_game_over: Cache l'écran Game Over.
        animate_death: Anime la mort du serpent (disparition progressive).
        animate_eat: Animation quand le serpent mange.
        cleanup: Nettoie toutes les ressources d'animation.
    """

    def __init__(self, screen: "_Screen"):
        """
        Initialise le gestionnaire d'animations.

        Args:
            screen: L'écran Turtle pour les animations.
        """
        self._screen = screen
        self._popup_turtles: List[turtle.Turtle] = []
        self._trail_turtles: List[turtle.Turtle] = []
        self._countdown_turtle: Optional[turtle.Turtle] = None
        self._game_over_turtle: Optional[turtle.Turtle] = None

        # Initialiser les turtles pour la trainée
        self._init_trail_turtles()

    def _init_trail_turtles(self):
        """Crée les turtles pour la trainée du serpent."""
        for i in range(TRAIL_LENGTH):
            t = turtle.Turtle()
            t.speed(0)
            t.shape("circle")
            t.shapesize(1.5 - (i * 0.2))  # Taille décroissante
            t.color(TRAIL_COLORS[min(i, len(TRAIL_COLORS) - 1)])
            t.penup()
            t.hideturtle()
            self._trail_turtles.append(t)

    def update_trail(self, positions: List[Tuple[float, float]]):
        """
        Met à jour la trainée visuelle du serpent.

        Args:
            positions: Liste des dernières positions du serpent.
        """
        # Prendre les dernières positions (en excluant la tête)
        trail_positions = positions[-(TRAIL_LENGTH + 2)                                    :-1] if len(positions) > 1 else []

        for i, trail_turtle in enumerate(self._trail_turtles):
            if i < len(trail_positions):
                pos = trail_positions[-(i + 1)] if i + \
                    1 <= len(trail_positions) else None
                if pos:
                    trail_turtle.goto(pos)
                    trail_turtle.showturtle()
                else:
                    trail_turtle.hideturtle()
            else:
                trail_turtle.hideturtle()

    def hide_trail(self):
        """Cache toute la trainée."""
        for t in self._trail_turtles:
            t.hideturtle()

    def show_score_popup(self, x: float, y: float, text: str = "+1"):
        """
        Affiche un popup animé qui monte et disparaît.

        Args:
            x: Position X du popup.
            y: Position Y du popup.
            text: Texte à afficher.
        """
        popup = turtle.Turtle()
        popup.speed(0)
        popup.color(COLOR_POPUP)
        popup.penup()
        popup.hideturtle()
        popup.goto(x, y + 20)

        self._popup_turtles.append(popup)

        # Démarrer l'animation
        self._animate_popup(popup, y + 20, 0)

    def _animate_popup(self, popup: turtle.Turtle, start_y: float, step: int):
        """
        Animation du popup montant.

        Args:
            popup: La turtle du popup.
            start_y: Position Y de départ.
            step: Étape actuelle de l'animation.
        """
        total_steps = int(POPUP_DURATION * 1000 / ANIMATION_FRAME_MS)

        if step >= total_steps:
            # Fin de l'animation
            popup.clear()
            if popup in self._popup_turtles:
                self._popup_turtles.remove(popup)
            return

        # Calculer la nouvelle position et opacité
        progress = step / total_steps
        new_y = start_y + (POPUP_RISE_DISTANCE * progress)

        # Mettre à jour le popup
        popup.clear()
        popup.goto(popup.xcor(), new_y)

        # Taille décroissante pour simuler la disparition
        font_size = int(24 * (1 - progress * 0.5))
        popup.write("+1", align="center", font=("Arial", font_size, "bold"))

        # Continuer l'animation
        self._screen.ontimer(
            lambda: self._animate_popup(popup, start_y, step + 1),
            ANIMATION_FRAME_MS
        )

    def show_countdown(self, on_complete: Callable):
        """
        Affiche le compte à rebours (3, 2, 1, GO!) rapide.

        Args:
            on_complete: Fonction à appeler quand le compte à rebours est terminé.
        """
        if not self._countdown_turtle:
            self._countdown_turtle = turtle.Turtle()
            self._countdown_turtle.speed(0)
            self._countdown_turtle.penup()
            self._countdown_turtle.hideturtle()

        self._countdown_turtle.clear()
        self._countdown_step(3, on_complete)

    def _countdown_step(self, count: int, on_complete: Callable):
        """
        Affiche une étape du compte à rebours.

        Args:
            count: Nombre actuel du compte à rebours.
            on_complete: Fonction à appeler à la fin.
        """
        if not self._countdown_turtle:
            return

        self._countdown_turtle.clear()
        self._countdown_turtle.goto(0, -30)

        if count > 0:
            # Couleur selon le chiffre
            if count == 3:
                color = "#F44336"  # Rouge
            elif count == 2:
                color = "#FF9800"  # Orange
            else:
                color = "#FFEB3B"  # Jaune

            # Contour noir
            self._countdown_turtle.color("black")
            for dx in [-3, 0, 3]:
                for dy in [-3, 0, 3]:
                    if dx != 0 or dy != 0:
                        self._countdown_turtle.goto(0 + dx, -30 + dy)
                        self._countdown_turtle.write(
                            str(count),
                            align="center",
                            font=("Arial", 100, "bold")
                        )

            # Afficher le nombre en couleur
            self._countdown_turtle.color(color)
            self._countdown_turtle.goto(0, -30)
            self._countdown_turtle.write(
                str(count),
                align="center",
                font=("Arial", 100, "bold")
            )
            self._screen.update()

            # Prochaine étape rapidement
            self._screen.ontimer(
                lambda: self._countdown_step(count - 1, on_complete),
                COUNTDOWN_DELAY
            )
        else:
            # Contour noir pour GO!
            self._countdown_turtle.color("black")
            for dx in [-3, 0, 3]:
                for dy in [-3, 0, 3]:
                    if dx != 0 or dy != 0:
                        self._countdown_turtle.goto(0 + dx, -30 + dy)
                        self._countdown_turtle.write(
                            "GO!",
                            align="center",
                            font=("Arial", 80, "bold")
                        )

            # Afficher "GO!" en couleur
            self._countdown_turtle.color(COLOR_GO)
            self._countdown_turtle.goto(0, -30)
            self._countdown_turtle.write(
                "GO!",
                align="center",
                font=("Arial", 80, "bold")
            )
            self._screen.update()

            # Effacer rapidement et démarrer le jeu
            self._screen.ontimer(
                lambda: self._finish_countdown(on_complete),
                GO_DELAY
            )

    def _finish_countdown(self, on_complete: Callable):
        """Termine le compte à rebours."""
        if self._countdown_turtle:
            self._countdown_turtle.clear()
        on_complete()

    def show_game_over(self, score: int, highscore: int, on_replay: Callable):
        """
        Affiche l'écran Game Over.

        Args:
            score: Score final du joueur.
            highscore: Meilleur score.
            on_replay: Fonction à appeler pour rejouer.
        """
        self._game_over_visible = True

        if not self._game_over_turtle:
            self._game_over_turtle = turtle.Turtle()
            self._game_over_turtle.speed(0)
            self._game_over_turtle.penup()
            self._game_over_turtle.hideturtle()

        self._game_over_turtle.clear()

        # Titre "GAME OVER" avec contour
        self._game_over_turtle.color("black")
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    self._game_over_turtle.goto(0 + dx, 60 + dy)
                    self._game_over_turtle.write(
                        "GAME OVER", align="center", font=("Arial", 50, "bold"))
        self._game_over_turtle.color(COLOR_GAME_OVER)
        self._game_over_turtle.goto(0, 60)
        self._game_over_turtle.write(
            "GAME OVER", align="center", font=("Arial", 50, "bold"))

        # Score avec contour
        self._game_over_turtle.color("black")
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    self._game_over_turtle.goto(0 + dx, 10 + dy)
                    self._game_over_turtle.write(
                        f"Score: {score}", align="center", font=("Arial", 28, "bold"))
        self._game_over_turtle.color("#FFEB3B")  # Jaune vif
        self._game_over_turtle.goto(0, 10)
        self._game_over_turtle.write(
            f"Score: {score}", align="center", font=("Arial", 28, "bold"))

        # Highscore avec contour
        highscore_text = "Nouveau record!" if score >= highscore and score > 0 else f"Meilleur: {highscore}"
        highscore_color = "#4CAF50" if score >= highscore and score > 0 else "#90CAF9"
        highscore_font = ("Arial", 22, "bold") if score >= highscore and score > 0 else (
            "Arial", 22, "normal")

        self._game_over_turtle.color("black")
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    self._game_over_turtle.goto(0 + dx, -35 + dy)
                    self._game_over_turtle.write(
                        highscore_text, align="center", font=highscore_font)
        self._game_over_turtle.color(highscore_color)
        self._game_over_turtle.goto(0, -35)
        self._game_over_turtle.write(
            highscore_text, align="center", font=highscore_font)

        # Instructions pour rejouer avec contour
        self._game_over_turtle.color("black")
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    self._game_over_turtle.goto(0 + dx, -90 + dy)
                    self._game_over_turtle.write(
                        "[ESPACE] Rejouer", align="center", font=("Arial", 16, "bold"))
        self._game_over_turtle.color(COLOR_REPLAY_TEXT)
        self._game_over_turtle.goto(0, -90)
        self._game_over_turtle.write(
            "[ESPACE] Rejouer", align="center", font=("Arial", 16, "bold"))

        self._screen.update()

    def hide_game_over(self):
        """Cache l'écran Game Over."""
        self._game_over_visible = False
        if self._game_over_turtle:
            self._game_over_turtle.clear()

    def animate_death(self, body_turtles: List[turtle.Turtle], on_complete: Callable):
        """
        Anime la mort du serpent (disparition progressive).

        Args:
            body_turtles: Liste des segments du corps.
            on_complete: Fonction à appeler à la fin.
        """
        if not body_turtles:
            on_complete()
            return

        self._death_step(body_turtles, 0, on_complete)

    def _death_step(self, body_turtles: List[turtle.Turtle], step: int, on_complete: Callable):
        """
        Une étape de l'animation de mort.

        Args:
            body_turtles: Liste des segments.
            step: Étape actuelle.
            on_complete: Fonction à appeler à la fin.
        """
        if step >= len(body_turtles):
            on_complete()
            return

        # Cacher un segment
        segment = body_turtles[-(step + 1)]
        segment.hideturtle()

        # Prochaine étape
        self._screen.ontimer(
            lambda: self._death_step(body_turtles, step + 1, on_complete),
            DEATH_ANIMATION_DELAY
        )

    def animate_eat(self, x: float, y: float):
        """
        Animation quand le serpent mange.

        Args:
            x: Position X.
            y: Position Y.
        """
        # Afficher le popup +1
        self.show_score_popup(x, y)

    def cleanup(self):
        """Nettoie toutes les ressources d'animation."""
        # Nettoyer les popups
        for popup in self._popup_turtles:
            try:
                popup.clear()
                popup.hideturtle()
            except (turtle.TurtleGraphicsError, Exception):
                # Ignorer toutes les erreurs liées à la destruction de la fenêtre
                pass
        self._popup_turtles.clear()

        # Nettoyer la trainée
        for t in self._trail_turtles:
            try:
                t.hideturtle()
            except (turtle.TurtleGraphicsError, Exception):
                pass

        # Nettoyer le compte à rebours
        if self._countdown_turtle:
            try:
                self._countdown_turtle.clear()
            except (turtle.TurtleGraphicsError, Exception):
                pass

        # Nettoyer game over
        if self._game_over_turtle:
            try:
                self._game_over_turtle.clear()
            except (turtle.TurtleGraphicsError, Exception):
                pass
