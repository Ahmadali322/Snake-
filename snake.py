import tkinter
import random
import gamedata
from PIL import Image, ImageTk

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

# to define snake and food values

class Tile:
    def __init__ (self, x, y):
        self.x = x
        self.y = y

# VARIABLE DECLARATION

# initializing window

window = tkinter.Tk()
window.title("Snake By Ahmad Ali")
# window.resizable(False, False)

# Set canvas for game

canvas = tkinter.Canvas(window, bg="black", width = WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth= 0, highlightthickness= 0)
canvas.pack()
window.update()

# to always open the window in center of screen

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# centeralize the game window

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Elements value

snake_start = random.randint(0,25-1)
food_start = random.randint(0,25-1)

while snake_start == food_start:
    food_start = random.randint(0,25-1)

snake = Tile(snake_start*TILE_SIZE, snake_start*TILE_SIZE) # Snake's Head
food = Tile(food_start*TILE_SIZE, food_start*TILE_SIZE) #food

velocityX = 0
velocityY= 0

# controls

up_controls = ['w', 'W', 'Up']
down_controls = ['s', 'S', 'Down']
left_controls = ['a', 'A', 'Left']
right_controls = ['d', 'D', 'Right']

# Miscelleneus

snake_body = []
game_over = False
score = 0
high_score = 0
oa_highscore = gamedata.highscore
oa_highplayer = gamedata.player
level = 1

# Load the semi-transparent image
bg_image = Image.open("transparent_background.png")
bg_image = bg_image.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

def change_direction(e): #e = Event
    global velocityX, velocityY, game_over, score, high_score, snake_body, food, snake, oa_highscore
    # print(e.keysym)
    if (game_over):
        if (e.keysym == "space"):
            # resetting Variables
            snake_start = random.randint(0,25-1)
            food_start = random.randint(0,25-1)

            while snake_start == food_start:
                food_start = random.randint(0,25-1)

            snake = Tile(snake_start*TILE_SIZE, snake_start*TILE_SIZE) # Snake's Head
            food = Tile(food_start*TILE_SIZE, food_start*TILE_SIZE) #food
            velocityX = 0
            velocityY= 0
            snake_body = []
            game_over = False
            score = 0
            oa_highscore = high_score
            high_score = 0
        else:
            return
    
    if (e.keysym in up_controls and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym in down_controls and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym in left_controls and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym in right_controls and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score, high_score, velocityY, velocityX
    
    if (game_over):
        return
    
    for i in range(1, level + 1):
        for tile in snake_body:
            if (snake.x == tile.x and snake.y == tile.y):
                if score - 1 <= 0:
                    velocityX = 0
                    velocityY = 0
                    game_over = True
                else:
                    score -= 1
    

    # detect collision with food
    if (snake.x == food.x and snake.y == food.y):
        for i in range(1, level + 1):
            snake_body.append(Tile(food.x, food.y))
            score += 1
        
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        for tile in snake_body:
            if (food.x == tile.x and food.y == tile.y):
                food.x = random.randint(0, COLS-1) * TILE_SIZE
                food.y = random.randint(0, ROWS-1) * TILE_SIZE

    # set high Score
    if score > high_score:
        high_score = score

    # check if food is in snake body
    for tile in snake_body:
        if (food.x == tile.x and food.y == tile.y):
            food.x = random.randint(0, COLS-1) * TILE_SIZE
            food.y = random.randint(0, ROWS-1) * TILE_SIZE

    # keep body attached to snake head
    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if(i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i -1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE
    
    # wrap around the screen if snake hits the boundary
    if snake.x >= WINDOW_WIDTH:
        snake.x = 0
    elif snake.x < 0:
        snake.x = WINDOW_WIDTH - TILE_SIZE
    if snake.y >= WINDOW_HEIGHT:
        snake.y = 0
    elif snake.y < 0:
        snake.y = WINDOW_HEIGHT - TILE_SIZE

#Drawing each frames of game
def draw():
    global snake, food, snake_body, score, high_score, game_over, oa_highscore
    move()
    
    canvas.delete('all')

    #draw Food1
    canvas.create_rectangle(food.x, food.y, food.x+TILE_SIZE, food.y+TILE_SIZE, fill = "red")

    # Draw Snake Bosy
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = 'dark green')

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x+TILE_SIZE, snake.y+TILE_SIZE, fill="lime green")

    # Display Game Over Message
    # oa_highscore = -1
    # game_over = True
    if (game_over):
        canvas.create_image(0, 0, anchor="nw", image=bg_photo)
        if high_score > oa_highscore:
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over\nHigh Score: {high_score}\n", fill = "white", justify = "center")
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 33, font = "Arial 20", text = "*NEW RECORD*", fill = "yellow")
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 58, font = "Arial 13", text = "(press space to restart)", fill = "white")
        else:
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over\nHigh Score: {high_score}", fill = "white", justify = "center")
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 45, font = "Arial 13", text = "(press space to restart)", fill = "white")
    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "white")
        
    #update frame
    window.after(100, draw) # 100ms = 10 frames / second. it will control speed basically

draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()
