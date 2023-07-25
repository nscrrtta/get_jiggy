from random import choice, randint, shuffle
from piece import Piece
from constants import *
import pygame


class Puzzle:
    
    def create_puzzle(self):

        # -1 = empty square
        #  0 = square not part of puzzle
        #  1 = occupied square

        while True:

            self.board  = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
            self.pieces = []

            shuffle(COLOURS)
            shuffle(SHAPES)

            for shape in SHAPES: # Guarantees each shape is unique

                # Flip and rotate shape randomly
                shape = flip(rotate(shape, randint(0,3)), randint(-1,1))

                where_shape_fits = self.get_where_shape_fits(shape)
                if len(where_shape_fits) == 0: continue

                self.add_piece_to_puzzle(shape, choice(where_shape_fits))
                if len(self.pieces) == NUM_PIECES: break

            if len(self.pieces) == NUM_PIECES and sum([row.count(-1) for row in self.board]) >= MIN_SQUARES: break
                
        self.organize_pieces()


    def get_where_shape_fits(self, shape: list) -> list:

        where_shape_fits = []
        shape_height = len(shape)
        shape_width  = len(shape[0])

        def shape_fits_here(row: int, col: int) -> bool:

            for y in range(shape_height):
                for x in range(shape_width):
                    if shape[y][x] == 1 and self.board[row+y][col+x] == -1:
                        return False
            return True

        for row in range(BOARD_ROWS-shape_height+1):
            for col in range(BOARD_COLS-shape_width+1):
                if shape_fits_here(row, col):
                    where_shape_fits.append([row,col])

        return where_shape_fits


    def add_piece_to_puzzle(self, shape: list, board_pos: list):

        row, col = board_pos
        shape_height = len(shape)
        shape_width  = len(shape[0]) 

        for y in range(shape_height):
            for x in range(shape_width):
                if shape[y][x] == 0: continue
                self.board[row+y][col+x] = -1
        
        colour_index = len(self.pieces)
        self.pieces.append(Piece(shape, COLOURS[colour_index], board_pos))


    def organize_pieces(self):

        # Organize pieces into two rows centered in window

        n = NUM_PIECES//2
        spacing = 0.7*35

        for row in range(2):

            pieces = self.pieces[row*n:(row+1)*n]
            
            x = 0 # Horizontal spacing between pieces
            y = 420 if row == 0 else 610

            for piece in pieces:
                x += len(piece.shape[0])*35+spacing

            x = (950-x+spacing)/2

            for piece in pieces:
                piece.home_pos   = [x,y]
                piece.screen_pos = [x,y]
                x += len(piece.shape[0])*35+spacing


    def draw(self, screen):

        screen.fill((80,80,80))

        # Draw board
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):

                if self.board[row][col] == 0: continue
                
                rect = pygame.Rect(
                    295+col*45+1,
                    30 +row*45+1,
                    45-2,
                    45-2
                )

                pygame.draw.rect(screen, (150,150,150), rect, width=0, border_radius=6)
                pygame.draw.rect(screen, (255,255,255), rect, width=1, border_radius=6)

        # Draw static pieces
        for piece in self.pieces:
            if piece.held: continue
            piece.draw(screen)

        # Draw held piece
        for piece in self.pieces:
            if not piece.held: continue
            piece.draw(screen)
            break


def rotate(shape: list, n: int, r=0) -> list:

    # Rotates shape clockwise n times (recursive)
    if n%4==r: return [row[:] for row in shape]
    return list(zip(*rotate(shape, n, r+1)[::-1]))


def flip(shape: int, direction: int) -> list:

    if direction == 0: return [row[:] for row in shape] # No flip
    if direction == 1: return [row[::-1] for row in shape] # Flip about y-axis
    if direction ==-1: return rotate(flip(rotate(shape,1),1),-1) # Flip about x-axis
