import pygame, os, json
from Interface import Interface
from Audio import Audio

class MenuPrincipal:
    def __init__(self, window):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Initialisation de la classe MenuPrincipal
        """

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

        # Afficher en bas à droite "Hackathon 2024 - Haute École en Hainaut Mons"
        fontCredits = pygame.font.SysFont(None, 20)
        credits_surface = fontCredits.render('Hackathon 2024 - Haute École en Hainaut Mons', True, (255, 255, 255))
        credits_rect = credits_surface.get_rect(center=(self.window_width - 180, self.window_height - 20))
        self.window.blit(credits_surface, credits_rect)

        # Afficher en bas à gauche "Inspiration du jeu: Trine"
        fontInspiration = pygame.font.SysFont(None, 20)
        inspiration_surface = fontInspiration.render('Inspiration du jeu: Trine', True, (255, 255, 255))
        inspiration_rect = inspiration_surface.get_rect(center=(100, self.window_height - 20))
        self.window.blit(inspiration_surface, inspiration_rect)

        # afficher au millieu de l'écran "Jeu par Anthony VERGEYLEN" et juste en dessous "Musique par Nathan Isembaert"
        fontCredits = pygame.font.SysFont(None, 20)
        credits_surface = fontCredits.render('Un jeu imaginé par:', True, (255, 255, 255))
        credits_rect = credits_surface.get_rect(center=(self.window_width // 2, self.window_height-105))
        self.window.blit(credits_surface, credits_rect)

        credits_surface = fontCredits.render('Vergeylen Anthony', True, (255, 255, 255))
        credits_rect = credits_surface.get_rect(center=(self.window_width // 2, self.window_height-80))
        self.window.blit(credits_surface, credits_rect)

        credits_surface = fontCredits.render('Duchesne Guillaume', True, (255, 255, 255))
        credits_rect = credits_surface.get_rect(center=(self.window_width // 2, self.window_height-60))
        self.window.blit(credits_surface, credits_rect)

        credits_surface = fontCredits.render('Nathan Isembaert', True, (255, 255, 255))
        credits_rect = credits_surface.get_rect(center=(self.window_width // 2, self.window_height-40))
        self.window.blit(credits_surface, credits_rect)

        credits_surface = fontCredits.render('Ulrich Wilfried Nguepi Kengoum', True, (255, 255, 255))
        credits_rect = credits_surface.get_rect(center=(self.window_width // 2, self.window_height-20))
        self.window.blit(credits_surface, credits_rect)




        self.button_width = 350
        self.button_height = 50
        self.button_margin = 5  # Margin for the black background
        self.button_spacing = 20  # Additional spacing between buttons

        save_slots = [] # (eg. ["1", "2", "3"])
        # get file saves.json, if file exist, get, else create
        if os.path.exists("saves.json"):
            with open("saves.json", "r") as f:
                # if file is empty, edit the file to {}
                if os.stat("saves.json").st_size == 0:
                    with open("saves.json", "w") as f:
                        json.dump({}, f)
                else :
                    save_slots = json.load(f)
        else:
            with open("saves.json", "w") as f:
                json.dump({}, f)
        

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
            'play': self.font.render('Créer une nouvelle partie', True, (255, 255, 255)),
            'quit': self.font.render('Quitter', True, (255, 255, 255))
        }

        for slot in save_slots:
            self.texts[f'load_{slot}'] = self.font.render(f'Charger la sauvegarde #{slot}', True, (255, 255, 255))

        self.button_clicked = False  # Initialize the button click state
        self.click_timer = 0  # Initialize the click timer

    def draw(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Dessine le menu principal
        """
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
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Gère les événements de la fenêtre
        """

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
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Boucle principale du menu principal et détection des actions
        """
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
                self.audio.stopMusic()
                menu_active = False
                save_slot = action.split('_')[1]
                print(f"On charge la sauvegarde #{save_slot}")
                # TODO: Load the save

                interface = Interface(self.window, save_slot)
                interface.run()

            pygame.time.wait(20)
            if self.button_clicked and pygame.time.get_ticks() - self.click_timer > 100:  # 100 ms delay
                self.button_clicked = False
