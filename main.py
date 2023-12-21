from tkinter import *
import random
import pygame

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
game_in_progress = False

welcome_screen_text = "Snake Game!\nMade By: RejectModders\nMade it for fun.\n\n" \
                      "Instructions:\n" \
                      "Use arrow keys to control the snake.\n" \
                      "Eat the red food to grow and earn points.\n" \
                      "Avoid running into the edges of the game window\n" \
                      "and colliding with yourself.\n\n" \
                      "Reminder... this also supports WASD keys!"

pygame.mixer.init()
eat_sound = pygame.mixer.Sound('eat_sound.mp3')
death_sound = pygame.mixer.Sound('death_sound.mp3')
background_sound = pygame.mixer.Sound('background_sound.mp3')

play_eat_sound = True
play_death_sound = True
play_background_sound = True
background_volume = 0.05
death_volume = 0.05
eat_volume = 0.05

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
        if play_eat_sound:
            eat_sound.play()
            eat_sound.set_volume(eat_volume)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(event):
    global direction
    key = event.keysym.lower()

    if key in ['left', 'a']:
        new_direction = 'left'
    elif key in ['right', 'd']:
        new_direction = 'right'
    elif key in ['up', 'w']:
        new_direction = 'up'
    elif key in ['down', 's']:
        new_direction = 'down'
    else:
        return

    if (new_direction == 'left' and direction != 'right') or \
       (new_direction == 'right' and direction != 'left') or \
       (new_direction == 'up' and direction != 'down') or \
       (new_direction == 'down' and direction != 'up'):
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    global game_in_progress
    if not game_in_progress:
        if play_death_sound:
            death_sound.play()
            death_sound.set_volume(death_volume)
        game_in_progress = True
        canvas.delete(ALL)
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                           font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 1.5,
                           font=('consolas', 13), text="Press the 'SPACE' key to restart", fill="white", tag="restart")
        window.bind('<space>', lambda event: restart_game())

def restart_game():
    global game_in_progress, snake, food, score, direction
    game_in_progress = False
    window.unbind('<space>')
    score = 0
    label.config(text="Score:{}".format(score))
    direction = 'down'
    snake = Snake()
    food = Food()
    window.after(1500, lambda: next_turn(snake, food))
    canvas.delete("gameover")
    canvas.delete("restart")

def welcome_screen():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 16), text=welcome_screen_text, fill="white", tag="welcome")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 1.4,
                       font=('consolas', 13), text="Press any key to start", fill="white", tag="welcome")

def start_game(event):
    global snake, food
    window.unbind('<Key>')
    canvas.delete("welcome")
    snake = Snake()
    food = Food()
    window.after(1500, lambda: next_turn(snake, food))
    window.bind('<Key>', change_direction)

def toggle_eat_sound():
    global play_eat_sound
    play_eat_sound = not play_eat_sound

def toggle_death_sound():
    global play_death_sound
    play_death_sound = not play_death_sound

def toggle_background_sound():
    global play_background_sound, background_volume
    play_background_sound = not play_background_sound
    if play_background_sound:
        background_sound.play(loops=-1)
        background_sound.set_volume(background_volume)
    else:
        background_sound.stop()

def update_eat_volume(value):
    global eat_volume
    eat_volume = float(value)
    if play_eat_sound:
        eat_sound.set_volume(eat_volume)

def update_death_volume(value):
    global death_volume
    death_volume = float(value)
    if play_death_sound:
        death_sound.set_volume(death_volume)

def update_background_volume(value):
    global background_volume
    background_volume = float(value)
    if play_background_sound:
        background_sound.set_volume(background_volume)

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.grid(row=0, column=0, columnspan=2)

background_sound_button = Button(window, text="Toggle Background Sound", command=toggle_background_sound)
background_sound_button.grid(row=1, column=0)

death_sound_button = Button(window, text="Toggle Death Sound", command=toggle_death_sound)
death_sound_button.grid(row=2, column=0)
eat_sound_button = Button(window, text="Toggle Eat Sound", command=toggle_eat_sound)
eat_sound_button.grid(row=3, column=0)

background_volume_slider = Scale(window, from_=0, to=1, resolution=0.01, orient=HORIZONTAL, label="Background Volume", command=update_background_volume)
background_volume_slider.set(background_volume)
background_volume_slider.grid(row=1, column=1)

death_volume_slider = Scale(window, from_=0, to=1, resolution=0.01, orient=HORIZONTAL, label="Death Volume", command=update_death_volume)
death_volume_slider.set(death_volume)
death_volume_slider.grid(row=2, column=1)

eat_volume_slider = Scale(window, from_=0, to=1, resolution=0.01, orient=HORIZONTAL, label="Eat Volume", command=update_eat_volume)
eat_volume_slider.set(eat_volume)
eat_volume_slider.grid(row=3, column=1)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.grid(row=4, column=0, columnspan=2)

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

toggle_background_sound()

welcome_screen()

window.bind('<Key>', start_game)

window.mainloop()
