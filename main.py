from puzzle import Puzzle
from constants import *
import pygame


pygame.init()
pygame.display.set_caption('Get Jiggy by Nick Sciarretta')
screen = pygame.display.set_mode((950, 800))


puzzle = Puzzle()
puzzle.create_puzzle()
pieces = puzzle.pieces
num_hints = NUM_HINTS


running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Select piece
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for piece in pieces:
                if piece.select(puzzle.board):
                    break

        # Move piece
        elif event.type == pygame.MOUSEBUTTONUP:
            for piece in pieces:
                if not piece.held: continue
                piece.release(puzzle.board)
                break

        elif event.type == pygame.KEYDOWN:

            # Spacebar = new puzzle
            if event.key == pygame.K_SPACE:
                puzzle.create_puzzle()
                pieces = puzzle.pieces
                num_hints = NUM_HINTS

            # Backspace = Remove all pieces from board
            elif event.key == pygame.K_BACKSPACE:
                for piece in pieces: 
                    if not piece.on_board: continue
                    piece.remove_from_board(puzzle.board)

            # H = show hint
            elif event.key == pygame.K_h and num_hints > 0:
                for piece in pieces: piece.show_hint = 1
                num_hints -= 1

    puzzle.draw(screen)
    pygame.display.update()


pygame.quit()