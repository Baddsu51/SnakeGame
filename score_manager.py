"""
Gestionnaire de score avec sauvegarde persistante
"""

import os
import turtle
from config import SCORE_FILE, SCORE_COLOR


class ScoreManager:
    """
    Gère le score actuel et le meilleur score (highscore).
    Affiche les scores à l'écran et sauvegarde le highscore.
    """

    def __init__(self):
        """Initialise le gestionnaire de score."""
        self._score = 0
        self._highscore = self._load_highscore()
        
        # Créer les affichages Turtle
        self._score_display = self._create_display(-390, 270)
        self._highscore_display = self._create_display(-390, 240)
        
        # Afficher les scores initiaux
        self._update_score_display()
        self._update_highscore_display()

    def _create_display(self, x: int, y: int) -> turtle.Turtle:
        """Crée un objet Turtle pour afficher du texte."""
        display = turtle.Turtle()
        display.speed(0)
        display.color(SCORE_COLOR)
        display.penup()
        display.hideturtle()
        display.goto(x, y)
        return display

    def _load_highscore(self) -> int:
        """
        Charge le highscore depuis le fichier.
        Retourne 0 si le fichier n'existe pas ou est corrompu.
        """
        try:
            if os.path.exists(SCORE_FILE):
                with open(SCORE_FILE, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        return int(content)
        except (ValueError, IOError, OSError) as e:
            print(f"Avertissement: Impossible de charger le highscore - {e}")
        return 0

    def save_highscore(self):
        """Sauvegarde le highscore dans le fichier."""
        try:
            # Créer le dossier si nécessaire
            score_dir = os.path.dirname(SCORE_FILE)
            if score_dir and not os.path.exists(score_dir):
                os.makedirs(score_dir, exist_ok=True)
            
            with open(SCORE_FILE, "w", encoding="utf-8") as f:
                f.write(str(self._highscore))
        except (IOError, OSError) as e:
            print(f"Avertissement: Impossible de sauvegarder le highscore - {e}")

    def _update_score_display(self):
        """Met à jour l'affichage du score actuel."""
        self._score_display.clear()
        self._score_display.write(
            f"Score: {self._score}",
            align="left",
            font=("Arial", 16, "bold")
        )

    def _update_highscore_display(self):
        """Met à jour l'affichage du highscore."""
        self._highscore_display.clear()
        self._highscore_display.write(
            f"Highscore: {self._highscore}",
            align="left",
            font=("Arial", 16, "bold")
        )

    @property
    def score(self) -> int:
        """Retourne le score actuel."""
        return self._score

    @property
    def highscore(self) -> int:
        """Retourne le meilleur score."""
        return self._highscore

    def add_point(self):
        """Ajoute un point au score et met à jour l'affichage."""
        self._score += 1
        self._update_score_display()

    def reset(self):
        """
        Réinitialise le score.
        Met à jour le highscore si nécessaire.
        """
        if self._score > self._highscore:
            self._highscore = self._score
            self.save_highscore()
            self._update_highscore_display()
        
        self._score = 0
        self._update_score_display()

    def cleanup(self):
        """Nettoie les ressources Turtle."""
        try:
            self._score_display.clear()
            self._highscore_display.clear()
        except turtle.TurtleGraphicsError:
            pass
