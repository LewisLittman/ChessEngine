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
    validMoves = gs.get_all_valid_moves()
    moveMade = False
    images = load_images()
    selected = ()
    selectedSquares = []
    promotion = False

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

        if moveMade:
            validMoves = gs.get_all_valid_moves()
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

def ask_promotion(screen, color):
    font = p.font.SysFont("Arial", 24)
    width, height = screen.get_size()
    overlay = p.Surface((width, height))
    overlay.set_alpha(200)
    overlay.fill((50, 50, 50))

    screen.blit(overlay, (0, 0))
    text = font.render("Promote to:", True, (255, 255, 255))
    screen.blit(text, (width//2 - text.get_width()//2, HEIGHT // 2 - 2 * SQ_SIZE // 2))

    # Load piece images or text labels
    pieces = ['Q', 'R', 'B', 'N']
    labels = ['Queen', 'Rook', 'Bishop', 'Knight']

    buttons = []
    button_width = 100
    button_height = 60
    margin = 20
    total_width = len(pieces) * (button_width + margin) - margin
    start_x = (width - total_width) // 2
    y = HEIGHT // 2 - SQ_SIZE // 2

    for i, label in enumerate(labels):
        rect = p.Rect(start_x + i*(button_width + margin), y, button_width, button_height)
        p.draw.rect(screen, (200, 200, 200), rect)
        txt = font.render(label, True, (0, 0, 0))
        screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
        buttons.append((rect, pieces[i]))

    p.display.flip()

    # Wait for click
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                quit()
            if event.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                for rect, piece_code in buttons:
                    if rect.collidepoint(pos):
                        return piece_code


if __name__ == "__main__":
    main()

