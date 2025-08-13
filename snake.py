from tkinter import *
import tkinter.messagebox as messagebox
import random

GAME_WIDTH = 660
GAME_HEIGHT = 660
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOR = "Green"
FOOD_COLOR = "Yellow"
BACKGROUND_COLOR = "SkyBlue"

# Define SPEED before using it
SPEED = 200


class Snake:
    def __init__(self):  # Corrected method name
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.body_ids = []  # Corrected attribute name
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.body_ids.append(square)

    def clear(self):
        for body_id in self.body_ids:
            canvas.delete(body_id)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def new_game():
    global score, snake, food, direction, game_running, high_score
    score = 0
    label.config(text="Score: {}".format(score))
    canvas.delete("food")
    canvas.delete("gameover")  # Add this line to clear the "gameover" items

    if snake:
        snake.clear()  # Clear the old snake's body

    snake = Snake()
    food = Food()
    direction = 'down'
    game_running = True  # Set game_running to True to start the game
    next_turn()  # Start the game loop


def next_turn():
    global snake, food, game_running
    if not game_running:
        return  # If the game is not running, do nothing

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

    snake.body_ids.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, high_score
        score += 1
        if score > high_score:
            high_score = score
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.body_ids[-1])
        del snake.body_ids[-1]

    if check_collisions():
        game_over()
    else:
        window.after(SPEED, next_turn)  # Use the 'SPEED' variable instead of level


def check_collisions():
    global snake
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def game_over():
    global game_running
    game_running = False
    canvas.delete("snake")
    canvas.delete("food")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")


def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def set_level(level):
    global SPEED
    if level == 'easy':
        SPEED = 250
    elif level == 'medium':
        SPEED = 100
    elif level == 'hard':
        SPEED = 10


def show_high_score():
    global high_score
    messagebox.showinfo("High Score", "The High Score is: {}".format(high_score))


# Initialize high score and level
high_score = 0

window = Tk()
window.title("Snake Xenzia")
window.resizable(False, False)

score = 0
direction = 'down'
game_running = True

label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

# Create a canvas with a background image
background_image = PhotoImage(file="V:\\File\\Documents\\vs\\uewfwe.png")  # Replace with the path to your image
canvas = Canvas(window, height=GAME_HEIGHT, width=GAME_WIDTH, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0)

canvas.create_image(0, 0, anchor=NW, image=background_image)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

# Create a menu bar
menu_bar = Menu(window)  # Set the background color for the menu bar
window.config(menu=menu_bar)
# Create a "Game" menu
game_menu = Menu(menu_bar, tearoff=0)  # Set the background color for the menu button
menu_bar.add_cascade(label="MENU", menu=game_menu)
# Add menu items to the "Game" menu with background color
game_menu.add_command(label="Start", command=new_game, activebackground="green")
game_menu.add_command(label="High Score", command=show_high_score, activebackground="blue")
# Create a "Level" submenu
level_submenu = Menu(game_menu, tearoff=0)  # Set the background color for the submenu button
game_menu.add_cascade(label="Level", menu=level_submenu, activebackground="orange")
# Add options to the "Level" submenu with background color
level_submenu.add_command(label="Easy", command=lambda: set_level('easy'), activebackground="green")
level_submenu.add_command(label="Medium", command=lambda: set_level('medium'), activebackground="yellow")
level_submenu.add_command(label="Hard", command=lambda: set_level('hard'), activebackground="red")

window.mainloop()