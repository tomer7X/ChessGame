import pygame
import sys
import os
import copy

import menuScreen


class ChessGame:

    def __init__(self, my_color, mod):
        # Initialize Pygame
        self.play_with_bot = mod
        self.play_as = my_color
        pygame.init()

        # Set up the display
        self.screen_size = (700, 700)  # Adjust the size as needed
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen.fill((255, 255, 255))  # Set the background color here (white in this case)
        pygame.display.set_caption("Chess Game")

        # Clock to control the frame rate
        self.clock = pygame.time.Clock()
        # Initialize the chess board
        self.board = self.initialize_board(self.play_as)

        # Variables to track selected piece and target square
        self.selected_piece = None
        self.legal_moves = []  # List to store legal moves for the selected piece
        self.all_legal_moves = []
        # Run the Pygame loop
        self.color_to_move = 'W'
        self.is_checkmate = False
        self.is_stalemate = False
        self.white_casting_pieces = [True, True, True]
        self.black_casting_pieces = [True, True, True]
        self.avaiable_enpassant = [False, -1, -1]
        self.last_move = {'piece': '  ', 'source': (-1, -1), 'dest': (-1, -1)}

        if self.play_with_bot:
            print(f'im playing as {self.play_as} with a bot')
        else:
            print(f"im playing as {self.play_as} with a friend")
        self.run()



    def initialize_board(self, playas):
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


    def mate(self):
        # Freeze the game window
        pygame.time.wait(1000)  # Wait for 1 second (adjust as needed)

        # Display a pop-up message
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        win_color = 'White' if self.last_move['piece'][0] == 'W' else 'Black'
        if self.is_stalemate:
            text_surface = font.render(f'Stalemate!', True, (255, 0, 0))  # Red color
        else:
            text_surface = font.render(f'Checkmate! {win_color} wins!', True, (255, 0, 0))  # Red color
        text_rect = text_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        # Wait for a few seconds before quitting
        pygame.time.wait(3000)  # Wait for 3 seconds (adjust as needed)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        menuScreen.MenuScreen()


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

    def is_square_threatened(self, square, color):
        row, col = square
        opponent_color = 'W' if color == 'B' else 'B'

        # Check for threats from pawns
        pawn_direction = 1 if color == 'W' else -1
        pawn_moves = [(pawn_direction, -1), (pawn_direction, 1)]
        for move in pawn_moves:
            move_x, move_y = move
            x, y = int(row) + move_x, col + move_y
            if 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] == opponent_color + 'P':
                return True

        # Check for threats from knights
        knight_moves = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]
        for move in knight_moves:
            move_x, move_y = move
            x, y = row + move_x, col + move_y
            if 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] == opponent_color + 'N':
                return True

        # Check for threats from bishops, rooks, and queens
        directions = [
            (0, -1), (0, 1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for dir in directions:
            move_x, move_y = dir
            i, j = row + move_x, col + move_y
            while 0 <= i < 8 and 0 <= j < 8:
                if self.board[i][j][0] == opponent_color:
                    if self.board[i][j][1] in ['B', 'R', 'Q']:
                        return True
                    else:
                        break
                elif self.board[i][j] != '  ':
                    break
                i, j = i + move_x, j + move_y

        # Check for threats from the opponent's king
        king_moves = [
            (1, 0), (0, 1), (1, 1), (1, -1),
            (-1, 1), (-1, -1), (-1, 0), (0, -1)
        ]
        for move in king_moves:
            move_x, move_y = move
            x, y = row + move_x, col + move_y
            if 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] == opponent_color + 'K':
                return True

        return False

    def has_white_pawn(self, row, col):
        if (0 <= row <= 7) and (0 <= col <= 7):
            return self.board[row][col] == 'WP'
        return False

    def has_white_piece(self, row, col):
        if (0 <= row <= 7) and (0 <= col <= 7):
            return self.board[row][col][0] == 'W'
        return False

    def print_board(self):
        for row in self.board:
            print(" ".join(row))
        print()

    def load_images(self):
        images = {}
        for piece in ['WP', 'BP', 'WR', 'BR', 'WN', 'BN', 'WB', 'BB', 'WQ', 'BQ', 'WK', 'BK','WS','BS']:
            image_path = os.path.join('images', f'{piece}.png')
            image = pygame.image.load(image_path).convert_alpha()
            images[piece] = pygame.transform.scale(image, (self.screen_size[0] // 8, self.screen_size[1] // 8))
        return images

    def still_in_check(self, source, dest, piece):
        board = copy.deepcopy(self.board)
        board[source[0]][source[1]] = '  '
        board[dest[0]][dest[1]] = piece
        if self.is_check(board, piece[0]):
            return True
        return False

    def avaiable_casting_moves(self, color):
        legal_moves = []
        if self.is_check(self.board, color):
            return []
        if self.white_casting_pieces[1] == True and color == 'W':
            #left rock white
            if self.white_casting_pieces[0] == True and self.board[7][1] == '  ' and self.board[7][2] == '  ' and self.board[7][3] == '  ' and not self.is_square_threatened((7, 2),'W') and not self.is_square_threatened((7, 3),'W'):
                legal_moves.append((7, 2))
            #right rock white
            if self.white_casting_pieces[2] == True and self.board[7][5] == '  ' and self.board[7][6] == '  ' and not self.is_square_threatened((7, 5), 'W') and not self.is_square_threatened((7, 6), 'W'):
                legal_moves.append((7, 6))
        elif self.black_casting_pieces[1] == True and color == 'B':
            # left rock black
            if self.black_casting_pieces[0] == True and self.board[0][1] == '  ' and self.board[0][2] == '  ' and \
                    self.board[0][3] == '  ' and not self.is_square_threatened((0, 2),'B') and not self.is_square_threatened((0, 3), 'B'):
                legal_moves.append((0, 2))
            # right rock white
            if self.black_casting_pieces[2] == True and self.board[0][5] == '  ' and self.board[0][
                6] == '  ' and not self.is_square_threatened((0, 5), 'B') and not self.is_square_threatened(
                    (0, 6), 'B'):
                legal_moves.append((0, 6))
        return legal_moves

    def is_check(self, board, color):
        # Find the king's position
        king_position = None
        for i in range(8):
            for j in range(8):
                if board[i][j] == color + 'K':
                    king_position = (i, j)
                    break

        if king_position is None:
            raise ValueError(f"No {color} king found on the board.")

        # Check for threats from opponent pieces
        opponent_color = 'W' if color == 'B' else 'B'

        # Check for threats from pawns
        pawn_direction = -1 if color == 'W' else 1
        pawn_moves = [(pawn_direction, -1), (pawn_direction, 1)]
        #pawns = self.find_pawns(opponent_color)
        for move in pawn_moves:
            move_x, move_y = move
            x, y = king_position[0] + move_x, king_position[1] + move_y
            if 0 <= x < 8 and 0 <= y < 8 and board[x][y] == opponent_color + 'P':
                return True

        # Check for threats from knights
        knight_moves = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]
        for move in knight_moves:
            move_x, move_y = move
            x, y = king_position[0] + move_x, king_position[1] + move_y
            if 0 <= x < 8 and 0 <= y < 8 and board[x][y] == opponent_color + 'N':
                return True

        # Check for threats from bishops, rooks, and queens
        directions = [
            (0, -1), (0, 1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for dir in directions:
            move_x, move_y = dir
            i, j = king_position[0] + move_x, king_position[1] + move_y
            while 0 <= i < 8 and 0 <= j < 8:
                if board[i][j][0] == opponent_color:
                    if board[i][j][1] == 'Q':
                        return True
                    elif board[i][j][1] == 'R' and (dir[0] == 0 or dir[1] == 0):
                        return True
                    elif board[i][j][1] == 'B' and abs(dir[0]) + abs(dir[1]) == 2:
                        return True
                    else:
                        break
                elif board[i][j] != '  ':
                    break
                i, j = i + move_x, j + move_y

        return False



    def generate_legal_moves(self, x, y, piece, flag=False):
        self.legal_moves = []
        check = False
        if self.is_check(self.board, piece[0]):
            check = True
        # -------------------------pawn
        if piece[1] == 'P':
            direction = -1 if piece[0] == 'W' else 1
            move_x = x + direction
            if 0 <= move_x < 8 and self.board[move_x][y] == '  ':
                if not self.still_in_check((x, y), (move_x, y), piece):
                    self.legal_moves.append((move_x, y))
                if ((piece[0] == 'W' and x == 6) or (piece[0] == 'B' and x == 1)) and self.board[move_x + direction][
                    y] == '  ':
                    if not self.still_in_check((x, y), (move_x + direction, y), piece):
                        self.legal_moves.append((move_x + direction, y))

            for move_y in [-1, 1]:
                new_col = y + move_y
                if 0 <= move_x < 8 and 0 <= new_col < 8:
                    target_piece = self.board[move_x][new_col]
                    if target_piece != '  ' and target_piece[0] != piece[0]:
                        if not self.still_in_check((x, y), (move_x, new_col), piece):
                            self.legal_moves.append((move_x, new_col))
            self.avaiable_enpassant = [False, -1, -1]
            # -------------------------en_passant:
            if self.last_move['piece'][0] != piece[0] and self.last_move['piece'][1] == 'P':
                if abs(self.last_move['source'][0] - self.last_move['dest'][0]) == 2:
                    if self.last_move['dest'][0] == x and abs(self.last_move['dest'][1] - y) == 1:
                        self.avaiable_enpassant = [True, self.last_move['dest'][0], self.last_move['dest'][1]]
                        if piece[0] == 'W':
                            if not self.still_in_check((x, y),
                                                       (self.last_move['dest'][0] - 1, self.last_move['dest'][1]),
                                                       piece):
                                self.legal_moves.append((self.last_move['dest'][0] - 1, self.last_move['dest'][1]))
                        else:
                            if not self.still_in_check((x, y),
                                                       (self.last_move['dest'][0] + 1, self.last_move['dest'][1]),
                                                       piece):
                                self.legal_moves.append((self.last_move['dest'][0] + 1, self.last_move['dest'][1]))

        # -------------------------bishop

        elif piece[1] == 'B':
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dir in directions:
                move_x, move_y = dir
                i, j = move_x + x, move_y + y
                while 0 <= i <= 7 and 0 <= j <= 7:
                    if self.board[i][j] == '  ' or piece[0] != self.board[i][j][0]:
                        if not self.still_in_check((x, y), (i, j), piece):
                            self.legal_moves.append((i, j))
                        if self.board[i][j] != '  ':
                            break
                    else:
                        break
                    i, j = move_x + i, move_y + j

        # -------------------------rock

        elif piece[1] == 'R':  # rock
            directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
            for dir in directions:
                move_x, move_y = dir
                i, j = move_x + x, move_y + y
                while 0 <= i <= 7 and 0 <= j <= 7:
                    if self.board[i][j] == '  ' or piece[0] != self.board[i][j][0]:
                        if not self.still_in_check((x, y), (i, j), piece):
                            self.legal_moves.append((i, j))
                        if self.board[i][j] != '  ':
                            break
                    else:
                        break
                    i, j = move_x + i, move_y + j

        # -------------------------night

        elif piece[1] == 'N':  # night
            directions = [(2, -1), (2, 1), (1, 2), (1, -2), (-2, -1), (-2, 1), (-1, 2), (-1, -2)]
            for dir in directions:
                move_x, move_y = dir
                i, j = move_x + x, move_y + y
                if 0 <= i <= 7 and 0 <= j <= 7:
                    if self.board[i][j] == '  ' or self.board[i][j][0] != piece[0]:
                        if not self.still_in_check((x, y), (i, j), piece):
                            self.legal_moves.append((i, j))

        # -------------------------Queen

        elif piece[1] == 'Q':  # Queen
            directions = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dir in directions:
                move_x, move_y = dir
                i, j = move_x + x, move_y + y
                while 0 <= i <= 7 and 0 <= j <= 7:
                    if self.board[i][j] == '  ' or piece[0] != self.board[i][j][0]:
                        if not self.still_in_check((x, y), (i, j), piece):
                            self.legal_moves.append((i, j))
                        if self.board[i][j] != '  ':
                            break
                    else:
                        break
                    i, j = move_x + i, move_y + j

        # -------------------------king

        elif piece[1] == 'K':  # king
            directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1), (-1, 0), (0, -1)]
            for dir in directions:
                move_x, move_y = dir
                i, j = move_x + x, move_y + y
                if 0 <= i <= 7 and 0 <= j <= 7:
                    if self.board[i][j] == '  ' or self.board[i][j][0] != piece[0]:
                        if not self.still_in_check((x, y), (i, j), piece):
                            self.legal_moves.append((i, j))
            casting_moves = self.avaiable_casting_moves(piece[0])
            for mv in casting_moves:
                self.legal_moves.append(mv)

        else:  # spiderman!
            for i in range(0, 8):
                for j in range(0, 8):
                    self.legal_moves.append((i, j))

        # add the piece moves to total
        if flag and len(self.legal_moves) != 0:
            self.all_legal_moves.append((piece, self.legal_moves))

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

                #after each move, we will see if there is check,checkmate,stalemate:
                #serach for all legal moves, if no legal moves,
                self.all_legal_moves = []
                color_can_be_checked = 'W' if self.last_move['piece'][0] == 'B' else 'B'
                for i in range(0, 8):
                    for j in range(0, 8):
                        if color_can_be_checked == self.board[i][j][0]:
                            self.generate_legal_moves(i, j, self.board[i][j], True)
                if len(self.all_legal_moves) == 0:
                    if self.is_check(self.board, color_can_be_checked):
                        self.is_checkmate = True
                    else:
                        self.is_stalemate = True

            else:
                # Clicking on the same piece again cancels the selection
                piece = self.board[row][col]
                if piece != '  ':
                    self.selected_piece = None
                    self.legal_moves = []

    def calculate_legal_moves(self, piece):
        # Calculate legal moves for the selected piece
        self.legal_moves = []
        if self.selected_piece and piece[0] == self.color_to_move:
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


            #check kings and rocks moves for casting
            if self.last_move['piece'] == 'WK':
                self.white_casting_pieces = [False, False, False]
            elif self.last_move['piece'] == 'BK':
                self.black_casting_pieces = [False, False, False]
            elif self.last_move['piece'][1] == 'R':
                if self.last_move['source'] == (0, 0):
                    self.black_casting_pieces[0] = False
                elif self.last_move['source'] == (0, 7):
                    self.black_casting_pieces[2] = False
                elif self.last_move['source'] == (7, 0):
                    self.white_casting_pieces[0] = False
                else:
                    self.white_casting_pieces[2] = False


            #move rock if casting has done
            if self.last_move['piece'][1] == 'K' and abs(self.last_move['source'][1] - self.last_move['dest'][1]) == 2:
                if self.last_move['dest'][1] == 6:
                    self.board[self.last_move['dest'][0]][5] = self.board[self.last_move['dest'][0]][7]
                    self.board[self.last_move['dest'][0]][7] = '  '
                else:
                    self.board[self.last_move['dest'][0]][3] = self.board[self.last_move['dest'][0]][0]
                    self.board[self.last_move['dest'][0]][0] = '  '



            # Check for pawn promotion for white pawn
            if (piece_to_move == 'WP' and self.target_square[0] == 0) or (piece_to_move == 'BP' and self.target_square[0] == 7):
                self.promote_pawn(piece_to_move[0])
            # Reset selected_piece and target_square

            #switch which color able to move next time.
            self.color_to_move = 'B' if self.color_to_move == 'W' else 'W'

            #check for checkmate


            self.selected_piece = None
            self.target_square = None

    def promote_pawn(self,piece_color):

        promotion_options = [piece_color+'Q', piece_color+'R', piece_color+'N', piece_color+'B',piece_color+'S']

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
                    if 0 <= chosen_option < 5 and chosen_high == 2:
                        if chosen_option == 0:
                            piece_kind = 'Q'
                        if chosen_option == 1:
                            piece_kind = 'R'
                        if chosen_option == 2:
                            piece_kind = 'N'
                        if chosen_option == 3:
                            piece_kind = 'B'
                        if chosen_option == 4:
                            piece_kind = 'S'
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

                # Determine the piece and its image based on the player's perspective
                if self.play_as == 'W':
                    piece = self.board[i][j]
                    self.screen.blit(square_surface, (j * square_size, i * square_size))
                else:
                    piece = self.board[7 - i][7 - j]
                    self.screen.blit(square_surface, ((7 - j) * square_size, (7 - i) * square_size))

                if piece != '  ':
                    piece_image = images[piece]
                    self.screen.blit(piece_image, (j * square_size, i * square_size))

                # Highlight legal moves if a piece is selected
                if self.selected_piece and (i, j) in self.legal_moves:
                    if not self.has_piece(i, j):
                        pygame.draw.circle(self.screen, (169, 169, 169), (
                        (j if self.play_as == 'W' else 7 - j) * square_size + square_size // 2,
                        (i if self.play_as == 'W' else 7 - i) * square_size + square_size // 2), square_size // 5)
                    else:
                        x_center = (j if self.play_as == 'W' else 7 -gi j) * square_size + square_size // 2
                        y_center = (i if self.play_as == 'W' else 7 - i) * square_size + square_size // 2
                        line_length = square_size // 2

                        pygame.draw.line(self.screen, (220, 5, 5), (x_center - line_length, y_center - line_length),
                                         (x_center + line_length, y_center + line_length), 2)
                        pygame.draw.line(self.screen, (220, 5, 5), (x_center - line_length, y_center + line_length),
                                         (x_center + line_length, y_center - line_length), 2)



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

            if self.is_checkmate or self.is_stalemate:
                 self.mate()

            pygame.display.flip()
            self.clock.tick(60)
