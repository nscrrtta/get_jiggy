from constants import *
import pygame


class Piece:

    def __init__(self, shape: list, colour: tuple, board_pos: list):

        self.shape  = shape
        self.colour = colour

        self.board_pos  = board_pos # Constant
        self.home_pos   = [0,0]     # Constant
        self.screen_pos = [0,0]     # Variable

        self.height = len(shape)
        self.width  = len(shape[0])

        self.held = self.on_board = self.show_hint = False
        

    def select(self, board) -> bool:
        
        a,b = self.screen_pos
        x,y = pygame.mouse.get_pos()
        sqr_size = 45 if self.on_board else 35

        def create_pos_dict():

            # Top-left corner of shape
            self.pos_dict = {(0,0): (a-x,b-y)}

            for row in range(self.height):
                for col in range(self.width):

                    if self.shape[row][col] == 0: continue

                    dr = b+row*45-y
                    dc = a+col*45-x
                
                    self.pos_dict[(col,row)] = (dc,dr)

        for row in range(self.height):
            for col in range(self.width):

                if self.shape[row][col] == 0: continue

                left   = a+col*sqr_size
                right  = left +sqr_size
                top    = b+row*sqr_size
                bottom = top + sqr_size

                if left < x < right and top < y < bottom: # Piece selected
                    if self.on_board: self.remove_from_board(board)
                    create_pos_dict()
                    self.held = True
                    return True

        return False
    

    def release(self, board: list):

        x,y = pygame.mouse.get_pos()
        a,b = self.pos_dict[(0,0)]

        # Math to determine which square on board
        # top-left square of piece is located
        r = (y+b- 30+45//2)//45
        c = (x+a-295+45//2)//45

        self.held = False

        for row in range(self.height):
            for col in range(self.width):

                if self.shape[row][col] == 0: continue

                new_row, new_col = int(row+r), int(col+c)

                # Out of bounds
                if not (0 <= new_col < BOARD_COLS and 0 <= new_row < BOARD_ROWS): return
                
                # Doesn't fit on board
                if board[new_row][new_col] != -1: return

        self.place_on_board(board)


    def place_on_board(self, board: list):

        x,y = pygame.mouse.get_pos()
        a,b = self.pos_dict[(0,0)]

        # Math to determine which square on board
        # top-left square of piece is located
        r = (y+b- 30+45//2)//45
        c = (x+a-295+45//2)//45

        for row in range(self.height):
            for col in range(self.width):

                if self.shape[row][col] == 0: continue
                board[int(row+r)][int(col+c)] = 1

        self.on_board = True
        self.screen_pos = [295+c*45, 30+r*45]
    

    def remove_from_board(self, board: list):

        a,b = self.screen_pos

        # Math to determine which square on board
        # top-left square of piece is located
        r = (b- 30)//45
        c = (a-295)//45
        
        for row in range(self.height):
            for col in range(self.width):

                if self.shape[row][col] == 0: continue
                board[int(row+r)][int(col+c)] = -1

        self.on_board = False
        self.screen_pos = self.home_pos[:]
    

    def draw(self, screen):

        sqr_size = 45

        if self.show_hint:
            row,col = self.board_pos
            x = col*sqr_size+295
            y = row*sqr_size+30

            self.show_hint += 1
            if self.show_hint == SHOW_HINT_TIME: self.show_hint = 0

        elif self.held: 
            x,y = pygame.mouse.get_pos()

        elif self.on_board: 
            x,y = self.screen_pos

        else:
            x,y = self.home_pos
            sqr_size = 35
            
        for row in range(self.height):
            for col in range(self.width):

                if self.shape[row][col] == 0: continue

                if self.held: dc,dr = self.pos_dict[(col,row)]
                else: dr,dc = row*sqr_size,col*sqr_size

                rect = pygame.Rect(dc+x+1, dr+y+1, sqr_size-2, sqr_size-2)
                pygame.draw.rect(screen, self.colour,   rect, width=0, border_radius=6)
                pygame.draw.rect(screen, (255,255,255), rect, width=1, border_radius=6)
