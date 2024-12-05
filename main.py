import pygame as pg
from random import randrange
import pygame.mouse
from buttons import Button
from globals import gui_font, menu_font, over_font, screen, resource_path
from pngs import (snake_body_col, snake_open_mouth_right, snake_closed_mouth_right,
                  snake_closed_mouth_left, snake_closed_mouth_up, snake_closed_mouth_down, food_png)
from snake_mouth_toggle import state_mapping
from save_load import save_highscore, load_highscore



pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
pg.mixer.init()

WINDOW = 750
TILE_SIZE = 50
clock = pg.time.Clock()
pg.display.set_caption('Snake')

RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

# Snake stuff
snake = snake_closed_mouth_right.get_rect()
snake_png = snake_closed_mouth_right
snake_png_open = snake_open_mouth_right
length = 1
snake.center = get_random_position()
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 100

# Snake mouth
open_mouth = False
mouth_timer = 0
mouth_interval = 300

# Movement restriction
move_timer = 0
move_interval = 50

# Food
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
button_save = Button('Save', 100, 45, (650, 648), 5)
button_load = Button('Load', 100, 45, (650, 700), 5)

# Sounds
main_menu_theme = pg.mixer.Sound(resource_path('sounds/Main_menu_theme.mp3'))
button_click = pg.mixer.Sound(resource_path('sounds/Button_sound.mp3'))
pause_theme = pg.mixer.Sound(resource_path('sounds/Pause_music.mp3'))
button_click = pg.mixer.Sound(resource_path('sounds/Button_sound.mp3'))
game_theme = pg.mixer.Sound(resource_path('sounds/Game_music.mp3'))

# Statements
sound = False
pause = False
gameover = False
last_input = None

# Main menu function
def main_menu():
    # Globals
    global sound, pause, gameover, snake_dir, move_timer, move_interval, highscore

    sound = False
    pause = False
    gameover = False
    snake_dir = (0, 0)

    while True:
        screen.fill('black')
        button_start.draw()
        button_quit.draw()
        button_load.draw()
        button_save.draw()


        highscore_txt = gui_font.render('HIGHSCORE: ' + str(highscore), True, (0, 255, 0))
        highscore_rect = highscore_txt.get_rect(center=(750 // 2, 20))
        title_txt = menu_font.render('SNAKE', True, (255, 255, 255))
        title_rect = title_txt.get_rect(center=(750 // 2, 200))

        screen.blit(highscore_txt, highscore_rect)
        screen.blit(title_txt, title_rect)

        if not sound:
            pg.mixer.Sound.play(main_menu_theme)
            main_menu_theme.set_volume(0.5)
            sound = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT or button_quit.pressed:
                pygame.mixer.Sound.play(button_click)
                pygame.quit()
                quit()
            if button_start.pressed:
                pg.mixer.Sound.play(button_click)
                button_start.pressed = False
                pg.mixer.Sound.stop(main_menu_theme)
                game_reset()
                return "game"

            # Save hs
            if button_save.pressed:
                pg.mixer.Sound.play(button_click)
                save_highscore(highscore, resource_path(resource_path("highscore.sav")))
                button_save.pressed = False
            # Load hs
            if button_load.pressed:
                pg.mixer.Sound.play(button_click)
                highscore = load_highscore(resource_path(resource_path("highscore.sav")))
                button_load.pressed = False

        pg.display.flip()
        clock.tick(60)

# Game function
def game_loop():
    # Globals
    global length, segments, highscore, score, gameover, pause, sound, snake_dir,\
        snake, time, last_input, snake_png, snake_png_open, mouth_interval, open_mouth,\
        mouth_timer, move_timer

    sound = False

    while True:
        # Game music
        if not sound:
            pygame.mixer.Sound.play(game_theme)
            game_theme.set_volume(0.3)
            sound = True

        screen.fill('#DEAA79')
        current_time = pg.time.get_ticks()

        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            # Keys
            if event.type == pg.KEYDOWN:
                move_time = pg.time.get_ticks()
                if move_time - move_timer > move_interval:
                    move_timer = move_time
                    if not pause and not gameover:
                        if event.key == pg.K_UP and last_input != 2:
                            snake_dir = (0, -TILE_SIZE)
                            snake_png = snake_closed_mouth_up
                            last_input = 1
                            move_time = 0
                        if event.key == pg.K_DOWN and last_input != 1:
                            snake_dir = (0, TILE_SIZE)
                            snake_png = snake_closed_mouth_down
                            last_input = 2
                            move_time = 0
                        if event.key == pg.K_LEFT and last_input != 4:
                            snake_dir = (-TILE_SIZE, 0)
                            snake_png = snake_closed_mouth_left
                            last_input = 3
                            move_time = 0
                        if event.key == pg.K_RIGHT and last_input != 3:
                            snake_dir = (TILE_SIZE, 0)
                            snake_png = snake_closed_mouth_right
                            last_input = 4
                            move_time = 0

                # Pause button
                if event.key == pg.K_ESCAPE:
                    pause = not pause

        # Drawing the snake
        for segment in segments[:-1]:
            screen.blit(snake_body_col, segment)
        screen.blit(snake_png, segments[-1])

        # Checking food
        if snake.center == food.center:
            food.center = get_random_position()
            length += 1
            score += 1
        while food.center in [segment.center for segment in segments]:
            food.center = get_random_position()

        # Drawing the food
        screen.blit(food_png, food)

        # Borders and eliminating it eating itself
        self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
        if self_eating:
            # Game over screen
            gameover = True

            pg.mixer.Sound.stop(game_theme)

            over_txt = over_font.render('GAME OVER', True, (255, 255, 255))
            over_rect = over_txt.get_rect(center=(750 // 2, 200))

            screen.blit(over_txt, over_rect)
            if score > highscore:
                highscore = score

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
            pg.mixer.pause()
            button_continue.draw()
            button_retry.draw()
            button_main.draw()
            if button_continue.pressed:
                pg.mixer.unpause()
                pause = False
                pg.mixer.Sound.play(button_click)
                button_continue.pressed = False
            elif button_retry.pressed:
                pg.mixer.Sound.play(button_click)
                pg.mixer.Sound.stop(game_theme)
                pause = False
                sound = False
                game_reset()
                button_retry.pressed = False
            elif button_main.pressed:
                pg.mixer.Sound.play(button_click)
                pg.mixer.Sound.stop(game_theme)
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

                # Border logic
                if snake.left < 0:
                    snake.right = WINDOW
                elif snake.right > WINDOW:
                    snake.left  = 0
                if snake.top < 0:
                    snake.bottom = WINDOW
                elif snake.bottom > WINDOW:
                    snake.top = 0

                new_head = pg.Rect(snake)
                segments.append(new_head)
                segments = segments[-length:]

        # Mouth animation
        if current_time - mouth_timer > mouth_interval:
            if not gameover and not pause:
                snake_png = state_mapping.get(snake_png, snake_png)
                open_mouth = not open_mouth
                mouth_timer = current_time


        pg.display.flip()
        clock.tick(60)

def game_reset():
    global length, snake_dir, segments, highscore, score, last_input

    snake.center, food.center = get_random_position(), get_random_position()
    length, snake_dir = 1, (0, 0)
    segments = [snake.copy()]
    highscore = score
    score = 0
    last_input = None



if __name__ == "__main__":
    current_state = "menu"  # Start in the menu
while True:
    if current_state == "menu":
        current_state = main_menu()
    elif current_state == "game":
        current_state = game_loop()


