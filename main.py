# main.py - entry point of program, displays main menu and handles game mode selection
import pygame as p
from GUI.main_menu import display_main_menu


p.init()

def main():
    mode = display_main_menu()
    # if mode == 'local':
    #     start_game(player_white=None, player_black=None)
    # elif mode == 'random':
    #     start_game(player_white=None, player_black=Random())
    # elif mode == 'minimax':
    #     start_game(player_white=None, player_black=Minimax())
    # else:
    #     print("Invalid mode selected. Exiting.")
    #     p.quit()

if __name__ == "__main__":
    main()