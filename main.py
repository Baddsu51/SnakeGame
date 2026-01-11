#!/usr/bin/env python3
"""
Snake Game - Jeu du serpent classique
=====================================

Un jeu Snake complet avec graphismes personnalisés, effets sonores
et système de highscore persistant.

Contrôles:
    Z - Haut
    S - Bas
    Q - Gauche
    D - Droite
    Échap - Pause
    X - Quitter

Auteur: Baddsu51
Version: 2.0 (refactorisation complète)
"""

from src.core.game import Game


def main():
    """Point d'entrée principal du jeu."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
