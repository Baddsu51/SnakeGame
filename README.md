# Snake Game in Python using Turtle

> A Snake game implemented in Python using the Turtle module.

Snake is a classic game where the player controls a snake that moves across a board, attempting to eat food (apples, in this case) to grow longer while avoiding hitting the board edges or biting its own tail. This project implements the Snake game in Python using the Turtle module for graphics.

![Game Preview](assets/demo.gif)

## 🌐 Note on Language

**Please note:** Since this project was a personal work originally created in French, the source code and game content have not been translated. While this README is here to help you navigate the project, you will encounter French in variable names, comments, and the user interface.

## 📖 About This Project

This project marks my first steps into software development. Created before I began my formal computer science studies, it represented a personal challenge to test my programming logic and Python knowledge.

Several years later, armed with the new skills acquired during my degree, I decided to improve this project by applying the best practices I've learned:

- **Architectural Overhaul**: Migration to a modular object-oriented architecture.
- **Code Organization**: Clear separation of concerns with a consistent folder structure.
- **Documentation**: Added docstrings and explanatory comments.
- **Centralized Configuration**: Improved management of constants and game settings.

This refactor demonstrates my evolution as a developer. While there is always room for improvement, this project illustrates my commitment to producing clean and maintainable code, even for a simple game initially developed in just a few days.

## Features

- Graphical display using Turtle.
- Snake control via ZQSD keys or arrow keys.
- Snake length increases upon eating food.
- Collision detection with board boundaries and the snake's own body.
- Real-time score display.
- Persistent high score saving.
- Pause menu (Esc key).
- Sound effects (compatible with Windows, macOS, and Linux).
- Modular object-oriented architecture.

## Prerequisites

- Python 3.8 or higher.
- pip (Python package manager).

## Installation

### Method 1: From Source

1. Clone this repository to your local machine:

```shell
git clone https://github.com/Baddsu51/SnakeGame
cd SnakeGame
```

2. (Optional) Create a virtual environment:

```shell
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

3. Install the required dependencies:

```shell
pip install -r requirements.txt
```

4. Run the game:

```shell
python main.py
```

### Method 2: Windows Executable

1. Download the latest [Release](https://github.com/Baddsu51/SnakeGame/releases).
2. Run `Snake_mainv3.exe`.

## Controls

| Key        | Action                 |
| ---------- | ---------------------- |
| Z (W) or ↑ | Move Up                |
| S or ↓     | Move Down              |
| Q (A) or ← | Move Left              |
| D or →     | Move Right             |
| Esc        | Pause / Resume         |
| X          | Quit Game              |
| Space      | Replay after Game Over |

## Dependencies

- **Pillow**: Image manipulation (PNG to GIF conversion) for Turtle.
- **pygame**: Cross-platform audio playback.

## Building an Executable

To create a Windows executable using PyInstaller:

```shell
pip install pyinstaller
python -m PyInstaller SnakeGame.spec
```

## License

This project is open source. You are free to use, modify, and distribute it.

## Author

**Baddsu51** - [GitHub](https://github.com/Baddsu51)
