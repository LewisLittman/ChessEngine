# GUI/main_menu.py - displays the main menu and handles user input for game mode selection
import pygame as p
import sys 

def display_main_menu():
    p.display.set_caption("Chess Engine - Main Menu")
    screen = p.display.set_mode((400, 300))
    font = p.font.SysFont("Sans-serif", 48)
    small_font = p.font.SysFont("Sans-serif", 24)

    options = [("1v1 Local", "local"),
               ("Play vs Random AI", "random"),
               ("Play vs Minimax AI", "minimax"),
               ("Quit", "quit")]

    selected_option = 0

    while True:
        screen.fill((30,30,30))

        title = font.render("Chess App", True, (255, 255, 255))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 30))

        for i, (text, _) in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (200, 200, 200)
            option_text = small_font.render(text, True, color)
            screen.blit(option_text, (screen.get_width()//2 - option_text.get_width()//2, 100 + i * 40))

        p.display.flip()

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.KEYDOWN:  # select game mode using arrow keys and enter - add feature later on to use mouse clicks
                if event.key == p.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == p.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == p.K_RETURN:
                    return options[selected_option][1]