"""
Gestionnaire de sons cross-platform utilisant pygame.mixer
"""

import os
from src.config import SOUND_EAT, SOUND_HIT

try:
    import pygame
except ImportError:
    pygame = None  # type: ignore


class SoundManager:
    """
    Gère la lecture des effets sonores du jeu.
    Utilise pygame.mixer pour la compatibilité cross-platform.

    Méthodes publiques:
        - play_eat(): Joue le son quand le serpent mange une pomme
        - play_hit(): Joue le son quand le serpent entre en collision
        - cleanup(): Libère les ressources audio
    """

    def __init__(self):
        """Initialise le système audio pygame."""
        self._initialized = False
        self._sound_eat = None
        self._sound_hit = None

        try:
            if pygame is None:
                raise ImportError("pygame n'est pas disponible")
            pygame.mixer.init(frequency=22050, size=-
                              16, channels=2, buffer=512)
            self._initialized = True
            self._load_sounds()
        except (ImportError, AttributeError, Exception) as e:
            print(f"Avertissement: Impossible d'initialiser l'audio - {e}")
            self._initialized = False

    def _load_sounds(self):
        """Charge les fichiers audio en mémoire."""
        if not self._initialized or pygame is None:
            return

        # Charger le son de manger
        if os.path.exists(SOUND_EAT):
            try:
                self._sound_eat = pygame.mixer.Sound(SOUND_EAT)
            except (Exception, FileNotFoundError, OSError) as e:
                print(
                    f"Avertissement: Impossible de charger le son 'eat' - {e}")

        # Charger le son de collision
        if os.path.exists(SOUND_HIT):
            try:
                self._sound_hit = pygame.mixer.Sound(SOUND_HIT)
            except (Exception, FileNotFoundError, OSError) as e:
                print(
                    f"Avertissement: Impossible de charger le son 'hit' - {e}")

    def play_eat(self):
        """Joue le son quand le serpent mange une pomme."""
        if self._initialized and self._sound_eat:
            try:
                self._sound_eat.play()
            except Exception:
                pass

    def play_hit(self):
        """Joue le son quand le serpent entre en collision."""
        if self._initialized and self._sound_hit:
            try:
                self._sound_hit.play()
            except Exception:
                pass

    def cleanup(self):
        """Libère les ressources audio."""
        if self._initialized and pygame is not None:
            try:
                pygame.mixer.quit()
            except Exception:
                pass
