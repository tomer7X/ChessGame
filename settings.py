import pygame
import sys


class SettingsScreen:
    def __init__(self, screen, background_image, background_rect, set_color, set_mod):
        self.screen = screen
        self.background_image = background_image
        self.background_rect = background_rect
        self.selected_color = set_color  # Default color
        self.play_with_bot = set_mod  # Default option

    def handle_settings(self):
        running = True
        selected_setting = 0 if not self.play_with_bot else 1  # Index 0 represents Play as color, Index 1 represents Play mode
        selected_color_index = 0 if self.selected_color == 'W' else 1  # Index 0 represents White

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
                            self.play_with_bot = not self.play_with_bot
                    elif event.key == pygame.K_RIGHT:
                        if selected_setting == 0:
                            selected_color_index = (selected_color_index + 1) % 2
                        else:
                            self.play_with_bot = not self.play_with_bot
                    elif event.key == pygame.K_RETURN:
                            self.selected_color = "W" if selected_color_index == 0 else "B"
                            print(self.play_with_bot)
                            running = False

            # Draw the settings menu
            self.screen.blit(self.background_image, self.background_rect)
            self.draw_settings(selected_setting, selected_color_index)
            pygame.display.flip()

            # return [self.selected_color, self.play_with_bot]

    def draw_settings(self, selected_setting, selected_color_index):
        font = pygame.font.Font(None, 36)

        # Draw background
        self.screen.blit(self.background_image, self.background_rect)

        # Draw title
        title_text = font.render("Settings", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Draw Play as color button
        play_as_button = pygame.draw.rect(self.screen, (50, 50, 50),
                                          (self.screen.get_width() // 2 - 150, 200, 300, 50))

        play_as_color = "White" if selected_color_index == 0 else "Black"
        play_as_text = font.render("Play as " + play_as_color, True, (255, 255, 255))
        play_as_rect = play_as_text.get_rect(center=play_as_button.center)
        self.screen.blit(play_as_text, play_as_rect)

        # Draw play mode selection button
        play_mode_button = pygame.draw.rect(self.screen, (50, 50, 50),
                                            (self.screen.get_width() // 2 - 150, 300, 300, 50))

        play_mode_text = font.render("Play with " + ("Friend" if not self.play_with_bot else "Bot"), True, (255, 255, 255))
        play_mode_rect = play_mode_text.get_rect(center=play_mode_button.center)
        self.screen.blit(play_mode_text, play_mode_rect)

        # Draw Back to Menu button
        back_to_menu_button = pygame.draw.rect(self.screen, (50, 50, 50),
                                               (self.screen.get_width() // 2 - 150, 400, 300, 50))

        back_to_menu_text = font.render("Press Enter to save", True, (255, 255, 255))
        back_to_menu_rect = back_to_menu_text.get_rect(center=back_to_menu_button.center)
        self.screen.blit(back_to_menu_text, back_to_menu_rect)

        # Draw arrow indicating selected setting
        arrow_size = 20
        arrow_center_x = self.screen.get_width() // 2 - 180
        arrow_center_y = 225 if selected_setting == 0 else 325
        pygame.draw.polygon(self.screen, (255, 255, 255), [(arrow_center_x, arrow_center_y - arrow_size),
                                                           (arrow_center_x + arrow_size, arrow_center_y),
                                                           (arrow_center_x, arrow_center_y + arrow_size)])

        pygame.display.flip()