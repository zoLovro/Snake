import pygame as pg
from random import randrange
import pygame.mouse
from buttons import Button
from globals import gui_font, menu_font, over_font, screen

pg.init()

WINDOW = 750
TILE_SIZE = 50
clock = pg.time.Clock()
pg.display.set_caption('Snake')

RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

snake = pg.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
length = 1
snake.center = get_random_position()
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 100

food = snake.copy()
food.center = get_random_position()

score = 0
highscore = 0

# Buttons
button_start = Button('Start game', 200, 45, (125, 500), 5)
button_quit = Button('Quit', 200, 45, (425, 500), 5)
button_main = Button('Main menu', 200, 45, (275, 455), 5)
button_continue = Button('Continue', 200, 45, (275, 255), 5)
button_retry = Button('Retry', 200, 45, (275, 355), 5)
button_quit_pause = Button('Quit', 200, 45, (275, 455), 5)

# Sounds
main_menu_theme = pg.mixer.Sound('./sounds/Main_menu_theme.mp3')
game_theme = pg.mixer.Sound('./sounds/Game_music.mp3')
pause_theme = pg.mixer.Sound('./sounds/Pause_music.mp3')
button_click = pg.mixer.Sound('./sounds/Button_sound.mp3')

# Statements
sound = False
pause = False
gameover = False

# Main menu function
def main_menu():
    # Globals
    global sound, pause, gameover, snake_dir
    sound = False
    pause = False
    gameover = False
    snake_dir = (0, 0)

    while True:
        screen.fill('black')
        button_start.draw()
        button_quit.draw()

        highscore_txt = gui_font.render('HIGHSCORE: ' + str(highscore), True, (0, 255, 0))
        highscore_rect = highscore_txt.get_rect(center=(750 // 2, 20))
        title_txt = menu_font.render('SNAKE', True, (255, 255, 255))
        title_rect = title_txt.get_rect(center=(750 // 2, 200))

        screen.blit(highscore_txt, highscore_rect)
        screen.blit(title_txt, title_rect)

        if not sound:
            pygame.mixer.Sound.play(main_menu_theme)
            sound = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT or button_quit.pressed:
                pygame.mixer.Sound.play(button_click)
                pygame.quit()
                quit()
            if button_start.pressed:
                button_start.pressed = False
                game_reset()
                return "game"

        pg.display.flip()
        clock.tick(60)

# Game function
def game_loop():
    # Globals
    global length, segments, highscore, score, gameover, pause, sound, snake_dir, snake, time

    while True:
        if not sound:
            pygame.mixer.Sound.play(game_theme)
            sound = True

        screen.fill('black')

        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            # Keys
            if event.type == pg.KEYDOWN:
                if not pause and not gameover:
                    if event.key == pg.K_w or event.key == pg.K_UP and snake_dir != (0, TILE_SIZE):
                        snake_dir = (0, -TILE_SIZE)
                    if event.key == pg.K_s or event.key == pg.K_DOWN and snake_dir != (0, -TILE_SIZE):
                        snake_dir = (0, TILE_SIZE)
                    if event.key == pg.K_a or event.key == pg.K_LEFT and snake_dir != (TILE_SIZE, 0):
                        snake_dir = (-TILE_SIZE, 0)
                    if event.key == pg.K_d or event.key == pg.K_RIGHT and snake_dir != (-TILE_SIZE, 0):
                        snake_dir = (TILE_SIZE, 0)

                # Pause button
                if event.key == pg.K_ESCAPE:
                    if pause:
                        pause = False
                    else:
                        pause = True

        # Drawing the snake
        [pg.draw.rect(screen, 'green', segment) for segment in segments]

        # Checking food
        if snake.center == food.center:
            food.center = get_random_position()
            length += 1
            score += 1
        elif food.center == segments:
            food.center = get_random_position()

        # Drawing the food
        pg.draw.rect(screen, 'red', food)

        # Borders and eliminating it eating itself
        self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
        if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
            # Game over screen
            gameover = True

            over_txt = over_font.render('GAME OVER', True, (255, 255, 255))
            over_rect = over_txt.get_rect(center=(750 // 2, 200))

            screen.blit(over_txt, over_rect)

            button_retry.draw()
            button_main.draw()
            if button_retry.pressed:
                pg.mixer.Sound.play(button_click)
                game_reset()
                gameover = False
                button_retry.pressed = False
            elif button_main.pressed:
                button_main.pressed = False
                return "menu"

        if pause and not gameover:
            button_continue.draw()
            button_retry.draw()
            button_main.draw()
            if button_continue.pressed:
                pause = False
                pg.mixer.Sound.play(button_click)
                button_continue.pressed = False
            elif button_retry.pressed:
                pause = False
                game_reset()
                button_retry.pressed = False
            elif button_main.pressed:
                button_main.pressed = False
                return "menu"

        # Score
        score_txt = gui_font.render('SCORE', True, (0, 255, 0))
        score_rect = score_txt.get_rect(center=(750 // 2, 25))
        score_val_txt = gui_font.render(str(score), True, (0, 255, 0))
        score_val_rect = score_val_txt.get_rect(center=(750 // 2, 55))

        screen.blit(score_txt, score_rect)
        screen.blit(score_val_txt, score_val_rect)

        # Moving the snake
        if not pause and not gameover:
            time_now = pg.time.get_ticks()
            if time_now - time > time_step:
                time = time_now
                snake.move_ip(snake_dir)
                segments.append(snake.copy())
                segments = segments[-length:]

        pg.display.flip()
        clock.tick(60)

def game_reset():
    global length, snake_dir, segments, highscore, score

    snake.center, food.center = get_random_position(), get_random_position()
    length, snake_dir = 1, (0, 0)
    segments = [snake.copy()]
    highscore = score
    score = 0



if __name__ == "__main__":
    current_state = "menu"  # Start in the menu
while True:
    if current_state == "menu":
        current_state = main_menu()
    elif current_state == "game":
        current_state = game_loop()
