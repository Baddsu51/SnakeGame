# Snake Game : Jeu du Snake avec Turtle

> Jeu du Snake classique implémenté en Python avec le module Turtle

Le jeu du Snake est un jeu classique où le joueur contrôle un serpent qui se déplace sur un plateau en essayant de manger des aliments pour grandir tout en évitant de se heurter aux bords du plateau ou de se mordre la queue. Ce projet implémente le jeu Snake en Python en utilisant le module Turtle pour les graphismes.

![Aperçu du jeu](https://i.imgur.com/XYzYEzG.png)

## Fonctionnalités

- Affichage graphique du jeu avec Turtle
- Contrôle du serpent avec les touches ZQSD (clavier AZERTY)
- Augmentation de la longueur du serpent en mangeant de la nourriture
- Détection de collision avec les bords du plateau et le serpent lui-même
- Affichage du score du joueur
- Sauvegarde persistante du meilleur score (highscore)
- Menu de pause (touche Échap)
- Effets sonores (compatible Windows, macOS et Linux)
- Architecture modulaire orientée objet

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

### Méthode 1 : Depuis les sources

1. Clonez ce référentiel sur votre machine locale :

   ```shell
   git clone https://github.com/Baddsu51/SnakeGame
   cd SnakeGame
   ```

2. (Optionnel) Créez un environnement virtuel :

   ```shell
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS / Linux
   source venv/bin/activate
   ```

3. Installez les dépendances requises :

   ```shell
   pip install -r requirements.txt
   ```

4. Lancez le jeu :

   ```shell
   python Snake_game.py
   ```

### Méthode 2 : Exécutable Windows

1. Téléchargez le dernier [Release](https://github.com/Baddsu51/SnakeGame/releases)
2. Exécutez `Snake_mainv3.exe`

## Contrôles

| Touche | Action |
|--------|--------|
| Z | Déplacer vers le haut |
| S | Déplacer vers le bas |
| Q | Déplacer vers la gauche |
| D | Déplacer vers la droite |
| Échap | Mettre en pause / Reprendre |
| X | Quitter le jeu |

## Structure du Projet

```
SnakeGame/
├── assets/                 # Ressources du jeu
│   ├── apple.png          # Image de la pomme
│   ├── carre_arrondi.png  # Image du corps du serpent
│   ├── grid.png           # Image de fond (grille)
│   ├── head_snake.png     # Image de la tête du serpent
│   ├── score.txt          # Sauvegarde du highscore
│   └── *.wav              # Fichiers audio
├── config.py              # Configuration et constantes
├── sound_manager.py       # Gestion audio cross-platform
├── score_manager.py       # Gestion des scores
├── apple.py               # Classe Apple
├── snake.py               # Classe Snake
├── game.py                # Classe Game principale
├── Snake_game.py          # Point d'entrée
├── requirements.txt       # Dépendances Python
└── README.md              # Ce fichier
```

## Dépendances

- **Pillow** : Manipulation des images PNG vers GIF pour Turtle
- **pygame** : Lecture des sons cross-platform

## Création d'un exécutable

Pour créer un exécutable Windows avec PyInstaller :

```shell
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/head_snake.ico --add-data "assets;assets" Snake_game.py
```

## Licence

Ce projet est open source. Vous êtes libre de l'utiliser, le modifier et le distribuer.

## Auteur

**Baddsu51** - [GitHub](https://github.com/Baddsu51)