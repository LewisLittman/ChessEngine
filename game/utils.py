# add functions that draw the board, pieces, game over etc
# Game/utils.py - utility functions for the chess app 

import pygame as p
from config.settings import game_info

def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    images = {}
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("Assets/" + piece + ".png"), (game_info.SQ_SIZE, game_info.SQ_SIZE))
    return images

def draw_board(screen):
    colors = [p.Color("white"), p.Color("cadetblue4")]
    for r in range(game_info.DIMENSION):
        for c in range(game_info.DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * game_info.SQ_SIZE, r * game_info.SQ_SIZE, game_info.SQ_SIZE, game_info.SQ_SIZE))

def draw_pieces(screen, board, images):
    for r in range(game_info.DIMENSION):
        for c in range(game_info.DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * game_info.SQ_SIZE, r * game_info.SQ_SIZE, game_info.SQ_SIZE * 0.8, game_info.SQ_SIZE * 0.8))

def square_highlight(screen, gs, validMoves, selectedSquare):
    if selectedSquare != ():
        r, c = selectedSquare
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((game_info.SQ_SIZE, game_info.SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('darkorchid'))
            screen.blit(s, (c * game_info.SQ_SIZE, r * game_info.SQ_SIZE))
            s.fill(p.Color('goldenrod1'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * game_info.SQ_SIZE, move.endRow * game_info.SQ_SIZE))

def draw_game_state(screen, gs, images, validMoves, selectedSquare):
    draw_board(screen)
    square_highlight(screen, gs, validMoves, selectedSquare)
    draw_pieces(screen, gs.board, images)

def ask_promotion(screen, color):
    font = p.font.SysFont("Sans serif", 24)
    width, height = screen.get_size()
    overlay = p.Surface((width, height))
    overlay.set_alpha(200)
    overlay.fill((50, 50, 50))

    screen.blit(overlay, (0, 0))
    text = font.render("Promote to:", True, (255, 255, 255))
    screen.blit(text, (width//2 - text.get_width()//2, game_info.HEIGHT // 2 - 2 * game_info.SQ_SIZE // 2))

    # Load piece images or text labels
    pieces = ['Q', 'R', 'B', 'N']
    labels = ['Queen', 'Rook', 'Bishop', 'Knight']

    buttons = []
    button_width = 100
    button_height = 60
    margin = 20
    total_width = len(pieces) * (button_width + margin) - margin
    start_x = (width - total_width) // 2
    y = game_info.HEIGHT // 2 - game_info.SQ_SIZE // 2

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

def game_over(screen, text):
    font = p.font.SysFont("Sans serif", 32)
    width, height = screen.get_size()
    overlay = p.Surface((width, height))
    overlay.set_alpha(200)
    overlay.fill((50, 50, 50))

    screen.blit(overlay, (0, 0))
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (width//2 - text_surface.get_width()//2, height//2 - text_surface.get_height()//2))
