# Snake Game : Jeu du Snake avec Turtle

> Jeu du Snake classique implémenté en Python avec le module Turtle

Le jeu du Snake est un jeu classique où le joueur contrôle un serpent qui se déplace sur un plateau en essayant de manger des aliments pour grandir tout en évitant de se heurter aux bords du plateau ou de se mordre la queue. Ce projet implémente le jeu Snake en Python en utilisant le module Turtle pour les graphismes.

![Aperçu du jeu](assets/demo.gif)

## 📖 À propos de ce projet

Ce projet marque mes premiers pas dans le développement logiciel. Créé au début de mes études d'informatique, il représentait à l'époque un défi personnel pour tester ma logique de programmation et mes connaissances en Python.

Plusieurs années plus tard, fort des compétences acquises durant mon cursus, j'ai décidé de revisiter ce projet pour le transformer et appliquer les bonnes pratiques apprises :

- **Refonte architecturale** : Migration vers une architecture orientée objet modulaire
- **Organisation du code** : Séparation claire des responsabilités avec une structure de dossiers cohérente
- **Documentation** : Ajout de docstrings et de commentaires explicatifs
- **Configuration centralisée** : Meilleure gestion des constantes et paramètres du jeu

Cette refonte témoigne de mon évolution en tant que développeur. Bien que perfectible, ce projet illustre mon engagement à produire du code propre et maintenable, même pour un jeu simple développé initialement en quelques jours.

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
   python main.py
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

## Dépendances

- **Pillow** : Manipulation des images PNG vers GIF pour Turtle
- **pygame** : Lecture des sons cross-platform

## Création d'un exécutable

Pour créer un exécutable Windows avec PyInstaller :

```shell
pip install pyinstaller
pyinstaller --onefile --windowed --name SnakeGame main.py
```

## Licence

Ce projet est open source. Vous êtes libre de l'utiliser, le modifier et le distribuer.

## Auteur

**Baddsu51** - [GitHub](https://github.com/Baddsu51)