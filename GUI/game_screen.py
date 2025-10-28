# GUI/game_screen.py - displays the game board and handles user input during the game

import pygame as p
from config.settings import game_info
from game.game_engine import GameState, Move
from game.utils import load_images, draw_board, draw_pieces, square_highlight, draw_game_state, game_over, ask_promotion

def start_game(player_white=None, player_black=None, game_info=None):
    # starts a chess game with given players (None for human) or a given AI /
    # engine object

    screen = p.display.set_mode((game_info.WIDTH, game_info.HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    validMoves = gs.get_all_valid_moves()
    moveMade = False
    running = True 
    images = load_images()
    selected = ()
    selectedSquares = []
    promotion = False

    while running:
        human_turn = (gs.whiteToMove and player_white is None) or (not gs.whiteToMove and player_black is None)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN and human_turn:
                location = p.mouse.get_pos()
                col = location[0] // game_info.SQ_SIZE
                row = location[1] // game_info.SQ_SIZE
                if selected == (row, col): # same square clicked twice = deselect
                    selected = ()
                    selectedSquares = []
                else: 
                    selected = (row, col)
                    selectedSquares.append(selected)
                if len(selectedSquares) == 2: # two squares selected = make move if valid
                    move = Move(selectedSquares[0], selectedSquares[1], gs.board)
                    print(move.get_chess_notation())
                    for validMove in validMoves:
                        if move == validMove:
                            gs.make_move(validMove)
                            moveMade = True
                            if validMove.pieceMoved[1] == 'P' and (validMove.endRow == 0 or validMove.endRow == 7):
                                promotion = True
                                promotionPiece = ask_promotion(screen, validMove.pieceMoved[0])
                                gs.make_promotion(validMove, promotionPiece)
                            break
                    selected = ()
                    selectedSquares = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    selected = ()
                    selectedSquares = []
                    moveMade = True
                    gs.checkMate = False
                    gs.staleMate = False
        
        if not human_turn and not gs.checkMate and not gs.staleMate:
            # AI move logic would go here
            pass


        if moveMade:
            validMoves = gs.get_all_valid_moves()
            moveMade = False
        
        draw_game_state(screen, gs, images, validMoves, selected)

        if gs.checkMate:
            game_over(screen, "Checkmate: " + ("Black" if gs.whiteToMove else "White") + " wins!")
        elif gs.staleMate:
            game_over(screen, "Stalemate: Draw!")
        
        clock.tick(game_info.MAX_FPS)
        p.display.flip()