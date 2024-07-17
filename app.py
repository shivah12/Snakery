from flask import Flask, request, jsonify, send_from_directory, render_template
import pygame
import random

app = Flask(__name__, static_url_path='', template_folder='templates')

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize Pygame mixer

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)

# Display settings
dis_width = 800
dis_height = 600
snake_block = 10
snake_speed = 15

# Set up fonts
font_path = "PressStart2P.ttf"
font_style_large = pygame.font.Font(font_path, 35)
font_style_medium = pygame.font.Font(font_path, 20)
font_style_small = pygame.font.Font(font_path, 20)
score_font = pygame.font.Font(font_path, 20)

# Load background images
start_bg = pygame.image.load('static/1.jpg')
start_bg = pygame.transform.scale(start_bg, (dis_width, dis_height))

game_bg = pygame.image.load('static/2.jpg')
game_bg = pygame.transform.scale(game_bg, (dis_width, dis_height))

# Load background music
pygame.mixer.music.load('static/music.mp3')

# Function to draw the snake
def our_snake(snake_block, snake_list, dis):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# Function to display messages on screen
def message(msg, color, y_displacement=0, font=font_style_large, dis=None):
    mesg = font.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2 + y_displacement))
    dis.blit(mesg, mesg_rect)

# Function to run the game loop
def gameLoop(dis):
    global snake_speed
    
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    clock = pygame.time.Clock()

    while not game_over:
        while game_close == True:
            dis.blit(game_bg, (0, 0))
            your_score(Length_of_snake - 1, y_displacement=-50, font=font_style_small, center=True, dis=dis)
            message("Try Again!", red, dis=dis)
            message("Press Q-Quit or C-Play Again", red, 50, font=font_style_medium, dis=dis)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(dis)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.blit(game_bg, (0, 0))
        pygame.draw.circle(dis, green, (int(foodx) + snake_block // 2, int(foody) + snake_block // 2), snake_block // 2)
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List, dis)
        your_score(Length_of_snake - 1, dis=dis)

        # Increase snake speed after score reaches 10
        if Length_of_snake > 10:
            snake_speed = 20

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Function to display score
def your_score(score, y_displacement=0, font=score_font, center=False, dis=None):
    value = font.render("Your Score: " + str(score), True, white)
    if center:
        value_rect = value.get_rect(center=(dis_width / 2, dis_height / 2 + y_displacement))
    else:
        value_rect = value.get_rect(topleft=(0, y_displacement))
    dis.blit(value, value_rect)

# Route to start the game
@app.route('/start-game')
def start_game_route():
    try:
        # Display start background and wait for Enter press
        display_start_screen()
        return 'Game started successfully'
    except Exception as e:
        return f'Error starting game: {str(e)}', 500

# Function to display the start screen with prompt to press Enter
def display_start_screen():
    dis = pygame.display.set_mode((dis_width, dis_height))
    dis.blit(start_bg, (0, 0))
    message("Start Game", white, y_displacement=-50, font=font_style_large, dis=dis)
    message("Press Enter to Start", white, y_displacement=50, font=font_style_medium, dis=dis)
    pygame.display.update()

    # Wait for Enter key press to start game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
                start_game()

# Function to start playing music and transition to game loop
def start_game():
    pygame.mixer.music.play(-1)  # Play music continuously
    gameLoop(pygame.display.set_mode((dis_width, dis_height)))

# Route to serve index.html (if needed)
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve static files (CSS, images, etc.)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
