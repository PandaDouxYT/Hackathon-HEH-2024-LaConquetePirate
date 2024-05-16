import pygame, os, json
from Interface import Interface
from Audio import Audio


class MenuPrincipal:
    def __init__(self, window):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Initialisation de la classe MenuPrincipal

        Arguments:
        - window: pygame.Surface

        Retourne:
        - Pas de retour

        """
        self.window = window
        self.window_width, self.window_height = self.window.get_size()
        self.font = pygame.font.Font(None, 36)

        self.audio = Audio()
        self.volume_level = self.load_volume()  # Charger le volume initial
        self.audio.set_global_volume(self.volume_level)
        self.audio.musicAmbiance("menu.mp3", True)

        # Set background to menuBackground.png
        background = pygame.image.load(
            os.path.join("assets", "img", "menuBackground.png")
        )
        self.window.blit(background, (0, 0))

        basicLogoWidth = 250
        self.logo = pygame.image.load(os.path.join("assets", "img", "logoheh.png"))
        self.logo = pygame.transform.scale(self.logo, (basicLogoWidth, int(basicLogoWidth * self.logo.get_height() / self.logo.get_width())))
        self.logo_rect = self.logo.get_rect(topright=(self.window_width - 10, 10))
        self.window.blit(self.logo, self.logo_rect)

        fontTitle = pygame.font.SysFont(None, 80)

        # Render title text in white
        title_surface = fontTitle.render("La Conquête Pirate !", True, (255, 255, 255))

        # Get the rectangle of the text and center it
        title_rect = title_surface.get_rect(center=(self.window_width // 2, 200))

        # Blit the title text on the window
        self.window.blit(title_surface, title_rect)

        # Afficher en bas à droite "Hackathon 2024 - Haute École en Hainaut Mons"
        fontCredits = pygame.font.SysFont(None, 20)
        credits_surface = fontCredits.render(
            "Hackathon 2024 - Haute École en Hainaut Mons", True, (255, 255, 255)
        )
        credits_rect = credits_surface.get_rect(
            center=(self.window_width - 180, self.window_height - 20)
        )
        self.window.blit(credits_surface, credits_rect)

        # Afficher en bas à gauche "Inspiration du jeu: Trine"
        fontInspiration = pygame.font.SysFont(None, 20)
        inspiration_surface = fontInspiration.render(
            "Inspiration du jeu: Trine", True, (255, 255, 255)
        )
        inspiration_rect = inspiration_surface.get_rect(
            center=(100, self.window_height - 20)
        )
        self.window.blit(inspiration_surface, inspiration_rect)

        # afficher au millieu de l'écran "Jeu par Anthony VERGEYLEN" et juste en dessous "Musique par Nathan Isembaert"
        fontCredits = pygame.font.SysFont(None, 20)
        credits_surface = fontCredits.render(
            "Un jeu imaginé par:", True, (255, 255, 255)
        )
        credits_rect = credits_surface.get_rect(
            center=(self.window_width // 2, self.window_height - 105)
        )
        self.window.blit(credits_surface, credits_rect)

        credits_surface = fontCredits.render("Vergeylen Anthony", True, (255, 255, 255))
        credits_rect = credits_surface.get_rect(
            center=(self.window_width // 2, self.window_height - 80)
        )
        self.window.blit(credits_surface, credits_rect)

        credits_surface = fontCredits.render(
            "Duchesne Guillaume", True, (255, 255, 255)
        )
        credits_rect = credits_surface.get_rect(
            center=(self.window_width // 2, self.window_height - 60)
        )
        self.window.blit(credits_surface, credits_rect)

        credits_surface = fontCredits.render("Nathan Isembaert", True, (255, 255, 255))
        credits_rect = credits_surface.get_rect(
            center=(self.window_width // 2, self.window_height - 40)
        )
        self.window.blit(credits_surface, credits_rect)

        credits_surface = fontCredits.render(
            "Ulrich Wilfried Nguepi Kengoum", True, (255, 255, 255)
        )
        credits_rect = credits_surface.get_rect(
            center=(self.window_width // 2, self.window_height - 20)
        )
        self.window.blit(credits_surface, credits_rect)

        self.button_width = 350
        self.button_height = 50
        self.button_margin = 5  # Margin for the black background
        self.button_spacing = 20  # Additional spacing between buttons

        self.maxSaves = 3  # Maximum number of saves
        save_slots = []  # (eg. ["1", "2", "3"])
        if os.path.exists("saves.json"):
            with open("saves.json", "r") as f:
                if os.stat("saves.json").st_size == 0:
                    with open("saves.json", "w") as f:
                        json.dump({}, f)
                else:
                    save_slots = json.load(f)
        else:
            with open("saves.json", "w") as f:
                json.dump({}, f)

        # Calculate the starting y position to center all buttons
        total_button_height = (
            self.button_height + self.button_margin + self.button_spacing
        ) * (2 + len(save_slots)) - self.button_spacing
        start_y = (self.window_height - total_button_height) // 2

        self.buttons = {
            "play": pygame.Rect(
                (self.window_width - self.button_width) // 2,
                start_y,
                self.button_width,
                self.button_height,
            ),
            "quit": pygame.Rect(
                (self.window_width - self.button_width) // 2,
                start_y
                + (self.button_height + self.button_margin + self.button_spacing)
                * (1 + len(save_slots)),
                self.button_width,
                self.button_height,
            ),
        }
        if len(save_slots) > 0:
            # mettre dans l'ordre 1, 2, 3 le dict save_slots
            save_slots = sorted(save_slots)
            for i, slot in enumerate(save_slots):
                self.buttons[f"load_{slot}"] = pygame.Rect(
                    (self.window_width - self.button_width) // 2,
                    start_y
                    + (self.button_height + self.button_margin + self.button_spacing)
                    * (i + 1),
                    self.button_width,
                    self.button_height,
                )
                self.buttons[f"delete_{slot}"] = pygame.Rect(
                    (self.window_width + self.button_width) // 2 + 20,
                    start_y
                    + (self.button_height + self.button_margin + self.button_spacing)
                    * (i + 1),
                    100,
                    self.button_height,
                )

        self.texts = {
            "play": self.font.render(
                "Créer une nouvelle partie", True, (255, 255, 255)
            ),
            "quit": self.font.render("Quitter", True, (255, 255, 255)),
        }

        for slot in save_slots:
            self.texts[f"load_{slot}"] = self.font.render(
                f"Charger la sauvegarde #{slot}", True, (255, 255, 255)
            )
            self.texts[f"delete_{slot}"] = self.font.render(
                "-", True, (255, 255, 255)
            )

        self.button_clicked = False  # Initialize the button click state
        self.click_timer = 0  # Initialize the click timer

        self.errorFont = pygame.font.Font(
            None, 35
        )  # Use SysFont to ensure regular (non-bold) font
        self.display_error_message = False
        self.error_message_text = self.errorFont.render(
            "Vous avez atteint le maximum de sauvegardes. ("
            + str(self.maxSaves)
            + "/"
            + str(self.maxSaves)
            + ")",
            True,
            (255, 0, 0),
        )
        self.error_message_duration = 3000  # en millisecondes
        self.error_message_start_time = 0

        # Control du volume
        self.volume_label = self.font.render("Volume", True, (255, 255, 255))
        self.volume_label_rect = self.volume_label.get_rect(
            midtop=(self.window_width // 2, start_y - 60)
        )

        self.volume_rect = pygame.Rect(
            (self.window_width - self.button_width) // 2,
            start_y - 30,
            self.button_width,
            20,
        )

        self.adjusting_volume = False

    def save_volume(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Sauvegarde la valeur du volume dans un fichier JSON
        
        Arguments:
        - Pas d'arguments
        
        Retourne:
        - Pas de retour
        
        """
        with open("settings.json", "w") as f:
            json.dump({"volume": self.volume_level}, f)

    def load_volume(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Charge la valeur du volume depuis un fichier JSON

        Arguments:
        - Pas d'arguments

        Retourne:
        - volume: float

        """

        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                return settings.get("volume", 1.0)
        except FileNotFoundError:
            return 1.0  # Valeur par défaut si le fichier n'existe pas

    def draw(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Dessine le menu principal

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour
        """
        # Dessiner les boutons
        for key, button in self.buttons.items():
            # Draw black background
            black_rect = pygame.Rect(
                button.left - self.button_margin,
                button.top - self.button_margin,
                button.width + 2 * self.button_margin,
                button.height + 2 * self.button_margin,
            )
            pygame.draw.rect(self.window, (0, 90, 90), black_rect)

            # Draw button
            pygame.draw.rect(self.window, (0, 128, 128), button)

            # Draw text
            text_rect = self.texts[key].get_rect(center=button.center)
            self.window.blit(self.texts[key], text_rect)

        # Afficher le volume
        self.window.blit(self.volume_label, self.volume_label_rect)
        pygame.draw.rect(
            self.window, (200, 200, 200), self.volume_rect, border_radius=10
        )
        handle_x = self.volume_rect.x + int(
            self.volume_level * (self.volume_rect.width - 20)
        )
        handle_rect = pygame.Rect(
            handle_x, self.volume_rect.y, 20, self.volume_rect.height
        )
        pygame.draw.rect(self.window, (0, 122, 255), handle_rect, border_radius=10)

        # Afficher le message d'erreur si nécessaire
        if self.display_error_message:
            elapsed_time = pygame.time.get_ticks() - self.error_message_start_time
            if elapsed_time < self.error_message_duration:
                error_message_rect = self.error_message_text.get_rect(
                    center=(self.window_width // 2, self.window_height - 160)
                )
                self.window.blit(self.error_message_text, error_message_rect)
            else:
                self.display_error_message = False

        pygame.display.update()

    def handle_events(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Gère les événements de la fenêtre

        Arguments:
        - Pas d'arguments

        Retourne:
        - action: str ou None

        """
        cursor_changed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.button_clicked:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for key, button in self.buttons.items():
                        if button.collidepoint(pos):
                            self.audio.musicAmbiance("clic.mp3")
                            self.button_clicked = (
                                True  # Set the flag to True when a button is clicked
                            )
                            self.click_timer = (
                                pygame.time.get_ticks()
                            )  # Record the time of the click
                            if key == "play":
                                # Check if maximum saves is reached
                                with open("saves.json", "r") as f:
                                    currentlySaves = json.load(f)
                                if len(currentlySaves) >= self.maxSaves:
                                    self.display_error_message = True
                                    self.error_message_start_time = (
                                        pygame.time.get_ticks()
                                    )
                                else:
                                    return "play"
                            elif key == "quit":
                                pygame.quit()
                                exit()
                            elif key.startswith("load_"):
                                save_slot = key.split("_")[1]
                                return f"load_{save_slot}"
                            elif key.startswith("delete_"):
                                save_slot = key.split("_")[1]
                                return f"delete_{save_slot}"
                    if self.volume_rect.collidepoint(pos):
                        self.adjusting_volume = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.adjusting_volume = False
                    self.save_volume()  # Sauvegarder le volume lorsque l'ajustement est terminé
            elif event.type == pygame.MOUSEMOTION:
                pos = event.pos
                cursor_changed = False
                if self.adjusting_volume:
                    relative_x = event.pos[0] - self.volume_rect.x
                    self.volume_level = max(
                        0, min(1, relative_x / (self.volume_rect.width - 20))
                    )
                    self.audio.set_global_volume(
                        self.volume_level
                    )  # Définir le volume global
                    cursor_changed = True
                else:
                    for key, button in self.buttons.items():
                        if button.collidepoint(pos):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            cursor_changed = True
                            break
                if not cursor_changed:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return None

    def run(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Boucle principale du menu principal et détection des actions

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour
        """
        menu_active = True
        while menu_active:
            self.draw()
            action = self.handle_events()
            if action == "play":
                menu_active = False
                print("Lancement du jeu...")

                pygame.time.wait(600)
                self.audio.stopMusic()
                # set mouse to default
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                interface = Interface(self.window)
                interface.run()
            elif action and action.startswith("load_"):
                self.audio.stopMusic()
                menu_active = False
                save_slot = action.split("_")[1]
                print(f"On charge la sauvegarde #{save_slot}")

                # Laisser le son du clic se jouer
                pygame.time.wait(600)
                self.audio.stopMusic()

                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                # TODO: Load the save completely
                interface = Interface(self.window, save_slot)
                interface.run()
            elif action and action.startswith("delete_"):
                save_slot = action.split("_")[1]
                with open("saves.json", "r") as f:
                    save_slots = json.load(f)
                if save_slot in save_slots:
                    del save_slots[save_slot]
                    with open("saves.json", "w") as f:
                        json.dump(save_slots, f)
                    print(f"Sauvegarde #{save_slot} supprimée")
                self.__init__(self.window)  # Reinitialize the menu to refresh the slots

            pygame.time.wait(20)
            if (
                self.button_clicked and pygame.time.get_ticks() - self.click_timer > 100
            ):  # 100 ms delay
                self.button_clicked = False
