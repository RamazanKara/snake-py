import pygame
import random

# Initialize Pygame
pygame.init()

# Game variables
width, height = 640, 480
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
food_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0

# Colors
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

# Game window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Game clock
clock = pygame.time.Clock()

# Sound effects
eat_sound = pygame.mixer.Sound("assets/eat.wav") 
collision_sound = pygame.mixer.Sound("assets/collision.wav") 

def show_game_over_screen():
    game_over_font = pygame.font.SysFont('arial', 50)
    game_over_surface = game_over_font.render('Game Over', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width / 2, height / 4)
    window.fill(black)
    window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    restart_game = False
    while not restart_game:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                restart_game = True

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Validate direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Update snake position
    if direction == 'UP':
        snake_pos[1] -= 10
    elif direction == 'DOWN':
        snake_pos[1] += 10
    elif direction == 'LEFT':
        snake_pos[0] -= 10
    elif direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 10
        food_spawn = False
        eat_sound.play()
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
    food_spawn = True

    # Wall collision detection
    if snake_pos[0] < 0 or snake_pos[0] > width-10 or snake_pos[1] < 0 or snake_pos[1] > height-10:
        collision_sound.play()
        show_game_over_screen()  # Display game over screen and wait for restart
        # Reset game variables for restart
        snake_pos = [100, 50]
        snake_body = [[100, 50], [90, 50], [80, 50]]
        direction = 'RIGHT'
        change_to = direction
        score = 0
        continue  # Restart the loop

    # Self-collision detection
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            collision_sound.play()
            show_game_over_screen()  # Display game over screen and wait for restart
            # Reset game variables for restart
            snake_pos = [100, 50]
            snake_body = [[100, 50], [90, 50], [80, 50]]
            direction = 'RIGHT'
            change_to = direction
            score = 0
            break

    # Drawing
    window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Displaying score
    font = pygame.font.SysFont('arial', 20)
    score_text = font.render(f'Score: {score}', True, white)
    window.blit(score_text, [0, 0])

    # Displaying creator text (adjusted position)
    creator_text = font.render('Created by Ramazan Kara', True, white)
    window.blit(creator_text, [50, height - 20])  # Adjusted X position

    pygame.display.flip()

    clock.tick(20)  # 20 frames per second

pygame.quit()
