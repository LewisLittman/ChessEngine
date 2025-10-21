# Main.py
# This is the main entry point for the chess engine application.

import pygame as p 
from GameEngine import GameState
from GameEngine import Move

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 20

def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    images = {}
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("Assets/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    return images

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    validMoves = gs.get_all_possible_moves()
    moveMade = False
    images = load_images()
    selected = ()
    selectedSquares = []

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if selected == (row, col):
                    selected = ()
                    selectedSquares = []
                else:
                    selected = (row, col)
                    selectedSquares.append(selected)
                if len(selectedSquares) == 2:   
                    move = Move(selectedSquares[0], selectedSquares[1], gs.board)
                    # print(move.get_chess_notation())
                    if move in validMoves:
                        gs.make_move(move)
                        moveMade = True
                    selected = ()
                    selectedSquares = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    selected = ()
                    selectedSquares = []
                    moveMade = True

        if moveMade:
            validMoves = gs.get_all_possible_moves()
            moveMade = False
        
        draw_game_state(screen, gs, images)
        clock.tick(MAX_FPS)
        p.display.flip()

def draw_game_state(screen, gs, images):
    draw_board(screen)
    draw_pieces(screen, gs.board, images)

def draw_board(screen):
    colors = [p.Color("white"), p.Color("cadetblue4")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
def draw_pieces(screen, board, images):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE * 0.8, SQ_SIZE * 0.8))


if __name__ == "__main__":
    main()