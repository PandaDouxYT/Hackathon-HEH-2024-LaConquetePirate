import pygame
import os
from Interface import Interface
from Audio import Audio

class MenuPrincipal:
    def __init__(self, window):
        self.window = window
        self.window_width, self.window_height = self.window.get_size()
        self.font = pygame.font.Font(None, 36)

        self.audio = Audio()
        self.audio.musicAmbiance("menu.mp3", True)

        # Set background to menuBackground.png
        background = pygame.image.load(os.path.join("assets", "img", "menuBackground.png"))
        self.window.blit(background, (0, 0))

        fontTitle = pygame.font.SysFont(None, 80)

        # Render title text in white
        title_surface = fontTitle.render('La Conquête Pirate !', True, (255, 255, 255))

        # Get the rectangle of the text and center it
        title_rect = title_surface.get_rect(center=(self.window_width // 2, 200))

        # Blit the title text on the window
        self.window.blit(title_surface, title_rect)

        self.button_width = 350
        self.button_height = 50
        self.button_margin = 5  # Margin for the black background
        self.button_spacing = 20  # Additional spacing between buttons

        # save_slots = []
        save_slots = ["2", "3", "4", "5", "6"]

        # Calculate the starting y position to center all buttons
        total_button_height = (self.button_height + self.button_margin + self.button_spacing) * (2 + len(save_slots)) - self.button_spacing
        start_y = (self.window_height - total_button_height) // 2

        self.buttons = {
            'play': pygame.Rect((self.window_width - self.button_width) // 2, 
                                start_y, 
                                self.button_width, self.button_height),
            'quit': pygame.Rect((self.window_width - self.button_width) // 2, 
                                start_y + (self.button_height + self.button_margin + self.button_spacing) * (1 + len(save_slots)), 
                                self.button_width, self.button_height)
        }
        if len(save_slots) > 0:
            for i, slot in enumerate(save_slots):
                self.buttons[f'load_{slot}'] = pygame.Rect(
                    (self.window_width - self.button_width) // 2, 
                    start_y + (self.button_height + self.button_margin + self.button_spacing) * (i + 1), 
                    self.button_width, self.button_height
                )

        self.texts = {
            'play': self.font.render('Lancer une partie', True, (255, 255, 255)),
            'quit': self.font.render('Quitter', True, (255, 255, 255))
        }

        for slot in save_slots:
            self.texts[f'load_{slot}'] = self.font.render(f'Charger la sauvegarde #{slot}', True, (255, 255, 255))

        self.button_clicked = False  # Initialize the button click state
        self.click_timer = 0  # Initialize the click timer

    def draw(self):
        for key, button in self.buttons.items():
            # Draw black background
            black_rect = pygame.Rect(button.left - self.button_margin,
                                     button.top - self.button_margin,
                                     button.width + 2 * self.button_margin,
                                     button.height + 2 * self.button_margin)
            pygame.draw.rect(self.window, (0, 90, 90), black_rect)

            # Draw button
            pygame.draw.rect(self.window, (0, 128, 128), button)

            # Draw text
            text_rect = self.texts[key].get_rect(center=button.center)
            self.window.blit(self.texts[key], text_rect)
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.button_clicked:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for key, button in self.buttons.items():
                        if button.collidepoint(pos):
                            self.button_clicked = True  # Set the flag to True when a button is clicked
                            self.click_timer = pygame.time.get_ticks()  # Record the time of the click
                            if key == 'play':
                                return 'play'
                            elif key == 'quit':
                                pygame.quit()
                                exit()
                            elif key.startswith('load_'):
                                save_slot = key.split('_')[1]
                                return f'load_{save_slot}'
        return None
    
    def run(self):
        menu_active = True
        while menu_active:
            self.draw()
            action = self.handle_events()
            if action == 'play':
                self.audio.stopMusic()  # Stop the music before launching the interface
                menu_active = False
                print("Lancement du jeu...")
                interface = Interface(self.window)
                interface.run()
            elif action and action.startswith('load_'):
                save_slot = action.split('_')[1]
                print(f"On charge la sauvegarde #{save_slot}")
            pygame.time.wait(20)
            if self.button_clicked and pygame.time.get_ticks() - self.click_timer > 100:  # 100 ms delay
                self.button_clicked = False
