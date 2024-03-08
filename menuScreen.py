import pygame
import sys
from chessGame import ChessGame

class MenuScreen:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Chess Game Menu")

        # Add menu items
        self.menu_items = ["Play", "Settings", "Exit"]
        self.selected_option = 0  # Index of the selected menu item

        self.background_image = pygame.image.load("images/background_design.png").convert()
        self.background_rect = self.background_image.get_rect()

        self.run()

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
            self.handle_settings()
        elif selected_item == "Exit":
            pygame.quit()
            sys.exit()

    def handle_settings(self):
        running = True
        selected_setting = 0  # Index 0 represents Play as color, Index 1 represents Play mode
        selected_color_index = 0  # Index 0 represents White
        play_with_bot = False  # Default option

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_setting = (selected_setting - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        selected_setting = (selected_setting + 1) % 2
                    elif event.key == pygame.K_LEFT:
                        if selected_setting == 0:
                            selected_color_index = (selected_color_index - 1) % 2
                        else:
                            play_with_bot = not play_with_bot
                    elif event.key == pygame.K_RIGHT:
                        if selected_setting == 0:
                            selected_color_index = (selected_color_index + 1) % 2
                        else:
                            play_with_bot = not play_with_bot
                    elif event.key == pygame.K_RETURN:
                        if selected_setting == 0:
                            selected_color = "W" if selected_color_index == 0 else "B"
                        else:
                            running = False

            # Draw the settings menu
            self.screen.blit(self.background_image, self.background_rect)
            self.draw_settings(selected_setting, selected_color_index, play_with_bot)
            pygame.display.flip()

        # After exiting the settings, you can use the selected_color and play_with_bot variables to start the game with the chosen settings.
        # For example, you can pass these values to your ChessGame constructor:
        # game = ChessGame(selected_color, play_with_bot)

    def draw_settings(self, selected_setting, selected_color_index, play_with_bot):
        font = pygame.font.Font(None, 36)

        # Draw background
        self.screen.blit(self.background_image, self.background_rect)

        # Draw title
        title_text = font.render("Settings", True, (150, 150, 150))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)

        if selected_setting == 0:
            # Draw Play as color button
            play_as_button = pygame.draw.rect(self.screen, (255, 255, 255),
                                              (self.screen.get_width() // 2 - 100, 200, 200, 50))

            play_as_color = "White" if selected_color_index == 0 else "Black"
            play_as_text = font.render("Play as " + play_as_color, True, (0, 0, 0))
            play_as_rect = play_as_text.get_rect(center=play_as_button.center)
            self.screen.blit(play_as_text, play_as_rect)
        else:
            # Draw play mode selection button
            play_mode_button = pygame.draw.rect(self.screen, (0, 255, 0),
                                                (self.screen.get_width() // 2 - 100, 300, 200, 50))

            play_mode_text = font.render("Play with " + ("Friend" if not play_with_bot else "Bot"), True, (0, 0, 0))
            play_mode_rect = play_mode_text.get_rect(center=play_mode_button.center)
            self.screen.blit(play_mode_text, play_mode_rect)

        # Draw Back to Menu button
        back_to_menu_button = pygame.draw.rect(self.screen, (0, 0, 255),
                                               (self.screen.get_width() // 2 - 100, 400, 200, 50))

        back_to_menu_text = font.render("Back to Menu", True, (255, 255, 255))
        back_to_menu_rect = back_to_menu_text.get_rect(center=back_to_menu_button.center)
        self.screen.blit(back_to_menu_text, back_to_menu_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_menu_input()
            self.screen.blit(self.background_image, self.background_rect)  # Draw the background image
            self.draw_menu()
            pygame.display.flip()