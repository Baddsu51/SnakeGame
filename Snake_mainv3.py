
import turtle
import time
from random import randint,choice
from PIL import Image
import winsound
import os,sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Chargement du son
path_hit_noice = resource_path('./assets/punch_whistle_noice.wav')
#path_eating_noice = 'apple_eating_noice.wav'
path_eating_noice = resource_path('./assets/apple_munch_noice.wav')


def jouer_son(path):
    winsound.PlaySound(path, winsound.SND_ASYNC)

# Charger l'image pomme
image_path = resource_path("./assets/apple.png")
image = Image.open(image_path)

# Réduire la taille de l'image si nécessaire
image.thumbnail((35,35))  # Ajustez les dimensions selon vos besoins

# Enregistrer l'image temporaire
apple_path = resource_path("./assets/temp_apple.gif")  # Chemin du fichier temporaire
image.save(apple_path)

# Créer une forme personnalisée à partir du fichier temporaire
turtle.Screen().register_shape(apple_path)

# Charger l'image corp
image_path = resource_path("./assets/carre_arrondi.png")
image = Image.open(image_path)

# Réduire la taille de l'image si nécessaire
image.thumbnail((40,40))  # Ajustez les dimensions selon vos besoins

# Enregistrer l'image temporaire
carre_path = resource_path("./assets/temp_carre.gif")  # Chemin du fichier temporaire
image.save(carre_path)

# Créer une forme personnalisée à partir du fichier temporaire
turtle.Screen().register_shape(carre_path)

def save_highscore():
    # Ouvrir le fichier en mode écriture
    with open(resource_path("./assets/score.txt"), "w") as fichier:
        # Écrire la variable dans le fichier
        fichier.write(str(highscore))

# Charger l'image
image_path = resource_path("./assets/head_snake.png")
image = Image.open(image_path)

# Réduire la taille de l'image si nécessaire
image.thumbnail((40,40))  # Ajustez les dimensions selon vos besoins

# Enregistrer l'image temporaire pour chaque direction
head_snake_nord = resource_path("./assets/temp_head_snake_nord.gif")  # Chemin du fichier temporaire
image.save(head_snake_nord)

image_sud = image.rotate(180)
head_snake_sud = resource_path("./assets/temp_head_snake_sud.gif")  # Chemin du fichier temporaire
image_sud.save(head_snake_sud)

image_est = image.rotate(270)
head_snake_est = resource_path("./assets/temp_head_snake_est.gif")  # Chemin du fichier temporaire
image_est.save(head_snake_est)

image_ouest = image.rotate(90)
head_snake_ouest = resource_path("./assets/temp_head_snake_ouest.gif")  # Chemin du fichier temporaire
image_ouest.save(head_snake_ouest)


# Créer une forme personnalisée à partir du fichier temporaire pour chaque direction
turtle.Screen().register_shape(head_snake_nord)
turtle.Screen().register_shape(head_snake_sud)
turtle.Screen().register_shape(head_snake_est)
turtle.Screen().register_shape(head_snake_ouest)

# Ouvrir le fichier en mode écriture
with open(resource_path('./assets/score.txt'), "r") as fichier:
    # Lire le contenu du fichier
    highscore = int(fichier.read())
    
# print('highscore', highscore)
# print(type(highscore))


# Création de la fenêtre de jeu
win = turtle.Screen()
win.title("Snake Game")
win.setup(width=800, height=600)
win.bgcolor("black")
win.bgpic(resource_path("./assets/grid.png"))
win.tracer(0)

# récupération coordonnées cases:
coordinates = []
grid_height = win.window_height()
grid_width = win.window_width()
size = 40
real_height = grid_height // 2
real_width = grid_width // 2
for x in range(size // 2, grid_width, size):
    for y in range(size // 2, grid_height, size):
        coordinates.append((x - real_width , y - real_height))

# Affichage des coordonnées
# for coord in coordinates:
#     print(coord)

# # Création d'un objet Turtle pour afficher les points
# point_turtle = turtle.Turtle()
# point_turtle.shape("circle")
# point_turtle.shapesize(0.2)
# point_turtle.color("white")
# point_turtle.penup()

# # Affichage des points à partir des coordonnées
# for coordinate in coordinates:
#     x, y = coordinate
#     point_turtle.goto(x, y)
#     point_turtle.stamp()

# Création de la tête du serpent
head = turtle.Turtle()
head.speed(0)
head.shape(head_snake_nord)
head.shapesize(1)
head.color("black")
head.penup()
head.direction = "Stop"
head.goto(-20, 0)

# Fonctions de mouvement
def move():
    s = 4
    if head.direction == "Up":
        y = head.ycor()
        head.shape(head_snake_sud)
        #head.sety(y + 40)
        head.setheading(90)
        head.speed(s)
        head.forward(40)

    elif head.direction == "Down":
        y = head.ycor()
        head.shape(head_snake_nord)
        # head.sety(y - 40)
        head.setheading(270)
        head.speed(s)
        head.forward(40)

    elif head.direction == "Left":
        x = head.xcor()
        head.shape(head_snake_est)
        # head.setx(x - 40)
        head.setheading(180)
        head.speed(s)
        head.forward(40)

    elif head.direction == "Right":
        x = head.xcor()
        head.shape(head_snake_ouest)
        # head.setx(x + 40)
        head.setheading(0)
        head.speed(s)
        head.forward(40)
        
        

def go_up():
    if head.direction != "Down":
        head.direction = "Up"


def go_down():
    if head.direction != "Up":
        head.direction = "Down"


def go_left():
    if head.direction != "Right":
        head.direction = "Left"


def go_right():
    if head.direction != "Left":
        head.direction = "Right"


win.listen()
win.onkeypress(go_up, "z")
win.onkeypress(go_down, "s")
win.onkeypress(go_left, "q")
win.onkeypress(go_right, "d")


turtle_size = 30
# Création de la pomme
def create_apple():
    apple = turtle.Turtle()
    apple.shape(apple_path)
    apple.shapesize(60,60)
    apple.color("red")
    apple.penup()
    x , y = choice(coordinates)
    # adjusted_x = x - turtle_size / 2
    # adjusted_y = y - turtle_size / 2
    apple.goto(x,y)
    return apple


# Création de l'affichage du score
score = 0

score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("black")
score_display.penup()
score_display.hideturtle()
score_display.goto(-390, 270)
score_display.write("Score: {}".format(score), align="left", font=("Arial", 16, "bold"))

highscore_display = turtle.Turtle()
highscore_display.speed(0)
highscore_display.color("black")
highscore_display.penup()
highscore_display.hideturtle()
highscore_display.goto(-390, 240)
highscore_display.write("Highscore: {}".format(highscore), align="left", font=("Arial", 16, "bold"))

def update_score():
    score_display.clear()  # Efface l'ancien score
    score_display.write("Score: {}".format(score), align="left", font=("Arial", 16, "bold"))


def update_highscore():
    highscore_display.clear()  # Efface l'ancien highscore
    highscore_display.write("Highscore: {}".format(highscore), align="left", font=("Arial", 16, "bold"))


def reset_game():
    # print('RESET GAME')
    global score, highscore, positions, body, L
    if score > highscore:
        highscore = score
        save_highscore()
        update_highscore()
    score = 0
    update_score()
    head.goto(-20, 0)
    head.direction = "Stop"
    apple.clear()
    for b in body:
        b.goto(1000, 1000)
    body = []
    positions = []
    L = 0
    
# Variable global
L = 0 #longueur du serpent
positions = []
positions.append(head.position())
body = []

# Variable pour la pause
paused = False

# Creation affichage Pause
pause = turtle.Turtle()
pause.speed(0)
pause.color("Black")
pause.penup()
pause.hideturtle()
pause.goto(1000, 1000)

# Fonction pour mettre en pause ou reprendre le jeu
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        pause.goto(0, -40)
        pause.write("Pause", align="center", font=("Arial", 120, "bold"))
    else:
        pause.clear()

# Assigner la fonction toggle_pause à la touche Echap
win.onkey(toggle_pause, "Escape")

# Activer la gestion des événements clavier
win.listen()

# Boucle principale du jeu
while True:
    if not paused:
        win.update()
        move()
        positions.append(head.position())
        if not "apple" in locals():
            apple = create_apple()
        # Vérifier si le serpent sort de l'écran
        if head.xcor() > 390 or head.xcor() < -390 or head.ycor() > 290 or head.ycor() < -290:
            jouer_son(path_hit_noice)
            # print('On sort de la bordure')
            reset_game()
    
        # Manger la pomme
        if apple.distance(head.position()) <= 35:
            jouer_son(path_eating_noice)
            score += 1
            L += 1
            update_score()
            x , y = choice(coordinates)
            while (x,y) in positions :
                x , y = choice(coordinates)
            # adjusted_x = x - turtle_size / 2
            # adjusted_y = y - turtle_size / 2
            apple.goto(x,y)
            
            # ajouter une partie du corp
            b =  turtle.Turtle()
            b.speed(0)
            b.shape(carre_path)
            sizeb = 40//20
            b.shapesize(sizeb)
            b.color('#779226')
            b.penup()
            b.direction = "Stop"
            b.goto(positions[-L])
            body.append(b)
            # Ajout de la taille
            
        if L != 0 :
            #déplacer le corp
            x, y = positions[-2]
            body[-1].goto(x,y)
            body.insert(0,body[-1])
            del body[-1]
            
        if len(positions) > L+1:
            del positions[:-L-1]
        
        # print(len(positions[:-1]))
        # print(head.position() in positions[:-1])
        if head.position() in positions[:-1] :
            jouer_son(path_hit_noice)
            # print('On se fonce dedans')
            reset_game()
            
        time.sleep(0.17)
        
    else:
        win.update()
        
turtle.clear()
turtle.done()

