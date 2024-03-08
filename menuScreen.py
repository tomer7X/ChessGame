import pygame
import sys
from chessGame import ChessGame
from settings import SettingsScreen


class MenuScreen:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.screen_size = (512, 512)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Chess Game Menu")

        # Add menu items
        self.menu_items = ["Play", "Settings", "Exit"]
        self.selected_option = 0  # Index of the selected menu item

        # Load and set background
        self.background_image, self.background_rect = self.load_and_set_background("images/background_design.png", 0.5)

        self.settings = ['W', 0]

        self.run()

    def load_and_set_background(self, image_path, zoom_factor):
        original_image = pygame.image.load(image_path).convert()
        original_rect = original_image.get_rect()

        # Create a new rect with scaled dimensions
        scaled_rect = original_rect.copy()
        scaled_rect.width = int(original_rect.width * zoom_factor)
        scaled_rect.height = int(original_rect.height * zoom_factor)

        # Center the scaled rect on the screen
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        scaled_rect.center = (center_x, center_y)

        # Scale the image and return both the image and rect
        scaled_image = pygame.transform.scale(original_image, (scaled_rect.width, scaled_rect.height))

        return scaled_image, scaled_rect

    def draw_menu(self):
        # Display the menu items
        font = pygame.font.Font(None, 36)
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            text = font.render(item, True, color)
            self.screen.blit(text, (self.screen_size[0] // 2 - text.get_width() // 2, i * 50 + 200))

    def handle_menu_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    self.handle_menu_selection()

    def handle_menu_selection(self):
        selected_item = self.menu_items[self.selected_option]
        if selected_item == "Play":
            # Start the chess game
            chess_game = ChessGame()
            chess_game.run()
        elif selected_item == "Settings":
            settings_screen = SettingsScreen(self.screen, self.background_image, self.background_rect)
            self.settings = settings_screen.handle_settings()
        elif selected_item == "Exit":
            pygame.quit()
            sys.exit()

    def run(self):
        while True:
            self.handle_menu_input()
            self.screen.blit(self.background_image, self.background_rect)  # Draw the background image
            self.draw_menu()
            pygame.display.flip()

# Example usage:
# menu = ChessGameMenu()
# menu.run()
