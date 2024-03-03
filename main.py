import pygame
import sys
import os

class ChessGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.screen_size = (700, 700)  # Adjust the size as needed
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen.fill((255, 255, 255))  # Set the background color here (white in this case)
        pygame.display.set_caption("Chess Game")

        # Clock to control the frame rate
        self.clock = pygame.time.Clock()
        # Initialize the chess board
        self.board = self.initialize_board()

        # Variables to track selected piece and target square
        self.selected_piece = None
        self.legal_moves = []  # List to store legal moves for the selected piece
        # Run the Pygame loop
        self.avaiable_enpassant = [False, -1, -1]
        self.last_move = {'piece': '  ', 'source': (-1, -1), 'dest': (-1, -1)}
        self.run()


    def initialize_board(self):
        # Create an 8x8 chess board with pieces in their initial positions
        board = [
            ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
            ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
            ['  '] * 8,  # Empty row
            ['  '] * 8,  # Empty row
            ['  '] * 8,  # Empty row
            ['  '] * 8,  # Empty row
            ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
            ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
        ]
        return board


    def has_piece(self, row, col):
        return self.board[row][col] != '  '

    def has_black_piece(self, row, col):
        if (0 <= row <= 7) and (0 <= col <= 7):
            return self.board[row][col][0] == 'B'
        return False

    def has_black_pawn(self, row, col):
        if (0 <= row <= 7) and (0 <= col <= 7):
            return self.board[row][col] == 'WP'
        return False

    def has_white_pawn(self, row, col):
        if (0 <= row <= 7) and (0 <= col <= 7):
            return self.board[row][col] == 'WP'
        return False

    def has_white_piece(self, row, col):
        if (0 <= row <= 7) and (0 <= col <= 7):
            return self.board[row][col][0] == 'W'
        return False

    def en_passant(self, piece, x ,y):
        if piece[0] == 'W':
            data = ['BP',1,3]
        if piece[0] == 'B':
            data = ['WP',6,4]
        if x != data[2]:
            return False
        if self.last_move == {'piece': data[0], 'source': (data[1], y), 'dest': (data[2], y)}:
            self.avaiable_enpassant = [True, data[2], y]
            return True
        self.avaiable_enpassant[0] = False
        return False
    def print_board(self):
        for row in self.board:
            print(" ".join(row))
        print()

    def load_images(self):
        images = {}
        for piece in ['WP', 'BP', 'WR', 'BR', 'WN', 'BN', 'WB', 'BB', 'WQ', 'BQ', 'WK', 'BK']:
            image_path = os.path.join('images', f'{piece}.png')
            image = pygame.image.load(image_path).convert_alpha()
            images[piece] = pygame.transform.scale(image, (self.screen_size[0] // 8, self.screen_size[1] // 8))
        return images



    def generate_legal_moves(self, x, y, piece):
        if piece == 'WP': #white pawn
            if not self.has_piece(x - 1, y):
                self.legal_moves.append((x - 1, y))
                if x == 6 and not self.has_piece(x - 2, y):
                    self.legal_moves.append((x - 2, y))
            if self.has_black_piece(x - 1, y - 1) or (self.en_passant(piece, x ,y - 1)):
                self.legal_moves.append((x - 1, y - 1))
            if self.has_black_piece(x - 1, y + 1) or (self.en_passant(piece, x ,y +1)):
                self.legal_moves.append((x - 1, y + 1))


        elif piece == 'BP': # black pawn
            if not self.has_piece(x + 1, y):
                self.legal_moves.append((x + 1, y))
                if x == 1 and not self.has_piece(x + 2, y):
                    self.legal_moves.append((x + 2, y))
            if self.has_white_piece(x + 1, y - 1) or (self.en_passant(piece, x, y - 1)):
                self.legal_moves.append((x + 1, y - 1))
            if self.has_white_piece(x + 1, y + 1) or (self.en_passant(piece, x,y+1)):
                self.legal_moves.append((x + 1, y + 1))

        elif piece[1] == 'B': #bishop
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dir in directions:
                move_x, move_y = dir
                i, j = move_x + x, move_y + y
                while 0 <= i <= 7 and 0 <= j <= 7:
                    if self.board[i][j] == '  '  or piece[0] != self.board[i][j][0]:
                        self.legal_moves.append((i,j))
                        if self.board[i][j] != '  ':
                            break
                    else:
                        break
                    i, j = move_x + i, move_y + j
        elif piece[1] == 'R': #rock
            directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
            for dir in directions:
                move_x, move_y = dir
                i, j = move_x + x, move_y + y
                while 0 <= i <= 7 and 0 <= j <= 7:
                    if self.board[i][j] == '  ' or piece[0] != self.board[i][j][0]:
                        self.legal_moves.append((i, j))
                        if self.board[i][j] != '  ':
                            break
                    else:
                        break
                    i, j = move_x + i, move_y + j
        elif piece[1] == 'N': #night
            directions = [(2, -1), (2, 1), (1, 2), (1, -2), (-2, -1), (-2, 1), (-1, 2), (-1, -2)]
            for dir in directions:
                move_x, move_y = dir
                i, j = move_x + x, move_y + y
                if 0 <= i <= 7 and 0 <= j <= 7:
                    if self.board[i][j] == '  ' or self.board[i][j][0] != piece[0]:
                        self.legal_moves.append((i,j))
        elif piece[1] == 'Q': #Queen
            directions = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dir in directions:
                move_x, move_y = dir
                i, j = move_x + x, move_y + y
                while 0 <= i <= 7 and 0 <= j <= 7:
                    if self.board[i][j] == '  ' or piece[0] != self.board[i][j][0]:
                        self.legal_moves.append((i, j))
                        if self.board[i][j] != '  ':
                            break
                    else:
                        break
                    i, j = move_x + i, move_y + j
        elif piece[1] == 'K': #king
            directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1), (-1, 0), (0, -1)]
            for dir in directions:
                move_x, move_y = dir
                i, j = move_x + x, move_y + y
                if 0 <= i <= 7 and 0 <= j <= 7:
                    if self.board[i][j] == '  ' or self.board[i][j][0] != piece[0]:
                        self.legal_moves.append((i, j))



    def handle_mouse_click(self, pos):
        square_size = self.screen_size[0] // 8
        col = pos[0] // square_size
        row = pos[1] // square_size

        if self.selected_piece is None:
            # No piece selected, check if the clicked square has a piece
            piece = self.board[row][col]
            if piece != '  ':
                if self.selected_piece == (row, col):
                    # Clicking on the same piece again cancels the selection
                    self.selected_piece = None
                    self.legal_moves = []
                else:
                    self.selected_piece = (row, col)
                    self.calculate_legal_moves(piece)
        else:
            # Move the selected piece to the clicked square if it's a legal move
            if (row, col) in self.legal_moves:
                self.target_square = (row, col)
                self.move_piece()

                if self.last_move['piece'][1] == 'P' and self.avaiable_enpassant[0] and (self.last_move['dest'] == (self.avaiable_enpassant[1]+1,self.avaiable_enpassant[2]) or self.last_move['dest'] == (self.avaiable_enpassant[1]-1,self.avaiable_enpassant[2])):
                    self.board[self.avaiable_enpassant[1]][self.avaiable_enpassant[2]] = '  '

            else:
                # Clicking on the same piece again cancels the selection
                piece = self.board[row][col]
                if piece != '  ':
                    self.selected_piece = None
                    self.legal_moves = []

    def calculate_legal_moves(self, piece):
        # Calculate legal moves for the selected piece
        self.legal_moves = []
        if self.selected_piece:
            self.generate_legal_moves(self.selected_piece[0], self.selected_piece[1], piece)

    def move_piece(self):
        if self.selected_piece and self.target_square:
            # Implement move validation logic here if needed
            piece_to_move = self.board[self.selected_piece[0]][self.selected_piece[1]]

            self.last_move['piece'] = piece_to_move
            self.last_move['source'] = self.selected_piece
            self.last_move['dest'] = self.target_square
            self.board[self.target_square[0]][self.target_square[1]] = piece_to_move
            self.board[self.selected_piece[0]][self.selected_piece[1]] = '  '



            # Check for pawn promotion for white pawn
            if (piece_to_move == 'WP' and self.target_square[0] == 0) or (piece_to_move == 'BP' and self.target_square[0] == 7):
                self.promote_pawn(piece_to_move[0])
            # Reset selected_piece and target_square

            self.selected_piece = None
            self.target_square = None

    def promote_pawn(self,piece_color):

        promotion_options = [piece_color+'Q', piece_color+'R', piece_color+'N', piece_color+'B']

        # Display promotion options
        promotion_images = [self.load_images()[option] for option in promotion_options]
        self.display_promotion_options(promotion_images,piece_color)

    def display_promotion_options(self, images,piece_color):
        square_size = self.screen_size[0] // 8

        while True:
            for i, image in enumerate(images):
                option_surface = pygame.Surface((square_size, square_size))
                option_surface.fill((255, 255, 255))
                option_surface.blit(image, (0, 0))
                self.screen.blit(option_surface, ((i + 2) * square_size, 4 * square_size))
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    chosen_option = (x // square_size) - 2
                    chosen_high = (y // square_size) - 2
                    piece_kind = ''
                    if 0 <= chosen_option < 4 and chosen_high == 2:
                        if chosen_option == 0:
                            piece_kind = 'Q'
                        if chosen_option == 1:
                            piece_kind = 'R'
                        if chosen_option == 2:
                            piece_kind = 'N'
                        if chosen_option == 3:
                            piece_kind = 'B'
                        self.board[self.target_square[0]][self.target_square[1]] = piece_color + piece_kind
                        return

    def display_board(self):
        # Display the chess board with graphics
        square_size = self.screen_size[0] // 8
        images = self.load_images()

        for i in range(8):
            for j in range(8):
                square_surface = pygame.Surface((square_size, square_size))

                # Use dark gray for black squares
                square_surface.fill((102, 51, 0) if (i + j) % 2 == 0 else (255, 255, 255))

                # Highlight legal moves if a piece is selected
                if self.selected_piece and (i, j) in self.legal_moves:
                    pygame.draw.circle(square_surface, (169, 169, 169), (square_size // 2, square_size // 2), square_size // 5)

                self.screen.blit(square_surface, (j * square_size, i * square_size))

                piece = self.board[i][j]
                if piece != '  ':
                    piece_image = images[piece]
                    self.screen.blit(piece_image, (j * square_size, i * square_size))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.handle_mouse_click(pygame.mouse.get_pos())

            self.display_board()

            pygame.display.flip()
            self.clock.tick(60)

# Test your initial setup
if __name__ == "__main__":
    game = ChessGame()
