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

        # Run the Pygame loop
        self.run()

    # ... (rest of the class remains unchanged)


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

    def load_images(self):
        images = {}
        for piece in ['WP', 'BP', 'WR', 'BR', 'WN', 'BN', 'WB', 'BB', 'WQ', 'BQ', 'WK', 'BK']:
            image_path = os.path.join('images', f'{piece}.png')
            image = pygame.image.load(image_path).convert_alpha()
            images[piece] = pygame.transform.scale(image, (self.screen_size[0] // 8, self.screen_size[1] // 8))
        return images

    def display_board(self):
        # Display the chess board with graphics
        square_size = self.screen_size[0] // 8
        images = self.load_images()

        for i in range(8):
            for j in range(8):
                square_surface = pygame.Surface((square_size, square_size))

                # Use dark gray for black squares
                square_surface.fill((102, 51, 0) if (i + j) % 2 == 0 else (255, 255, 255))

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

            self.display_board()

            pygame.display.flip()
            self.clock.tick(60)

# Test your initial setup
if __name__ == "__main__":
    game = ChessGame()
