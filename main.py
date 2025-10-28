# main.py - entry point of program, displays main menu and handles game mode selection
import pygame as p
from GUI.main_menu import display_main_menu
from GUI.run_game import start_game
from config.settings import GameInfo
from engines.random_engine import RandomEngine 

p.init()

def main():
    game_info = GameInfo()
    mode = display_main_menu()
    if mode == 'local':
        start_game(player_white=None, player_black=None, game_info=game_info)
    elif mode == 'random':
        start_game(player_white=None, player_black=RandomEngine('b'), game_info=game_info)
    # elif mode == 'minimax':
    #     start_game(player_white=None, player_black=Minimax())
    else:
        print("Invalid mode selected. Exiting.")
        p.quit()

if __name__ == "__main__":
    main()