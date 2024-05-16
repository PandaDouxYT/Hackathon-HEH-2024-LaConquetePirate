import pygame, os, json
from Audio import Audio
from Joueur import Joueur


class PauseMenu:
    def __init__(self, window, idOfLoadedGame, joueurActif, initial_volume=1.0):
        """
        QUI: Nathan Isembaert & Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Initialisation du menu de pause
        """
        self.audio = Audio()
        self.idOfLoadedGame = idOfLoadedGame
        self.joueurActif = joueurActif
        self.maxSaves = 3
        self.volume_level = self.load_volume()
        self.audio.set_global_volume(self.volume_level)  # Définir le volume initial

        pygame.font.init()
        self.window = window
        self.font = pygame.font.Font(pygame.font.match_font("Helvetica", bold=True), 20)
        self.title_font = pygame.font.Font(
            pygame.font.match_font("Helvetica", bold=True), 40
        )
        self.window_width, self.window_height = window.get_size()

        self.menu_width = 450
        self.menu_height = 400
        self.menu_x = (self.window_width - self.menu_width) // 2
        self.menu_y = (self.window_height - self.menu_height) // 2

        self.button_width = 260
        self.button_height = 50
        self.button_x = self.menu_x + (self.menu_width - self.button_width) // 2

        self.title_height = 60
        self.title_y = self.menu_y + 20

        button_positions = [
            self.title_y + self.title_height + 20,
            self.title_y + self.title_height + 80,
            self.title_y + self.title_height + 200,
            self.title_y + self.title_height + 260,
        ]

        self.buttons = {
            "resume": pygame.Rect(
                self.button_x,
                button_positions[0],
                self.button_width,
                self.button_height,
            ),
            "save": pygame.Rect(
                self.button_x,
                button_positions[1],
                self.button_width,
                self.button_height,
            ),
            "quit": pygame.Rect(
                self.button_x,
                button_positions[3],
                self.button_width,
                self.button_height,
            ),
        }

        self.texts = {
            "resume": self.font.render("Retour en jeu", True, (255, 255, 255)),
            "save": self.font.render("Sauvegarder la partie", True, (255, 255, 255)),
            "quit": self.font.render("Quitter le jeu", True, (255, 255, 255)),
        }

        # Control du volume
        self.volume_label = self.font.render("Son", True, (0, 0, 0))
        self.volume_label_rect = self.volume_label.get_rect(
            midtop=(self.menu_x + self.menu_width // 2, button_positions[1] + 70)
        )

        self.volume_rect = pygame.Rect(
            self.button_x, button_positions[1] + 110, self.button_width, 20
        )

        self.pause_text = self.title_font.render("- Menu -", True, (0, 0, 0))
        self.pause_text_rect = self.pause_text.get_rect(
            center=(
                self.menu_x + self.menu_width // 2,
                self.title_y + self.title_height // 2,
            )
        )

        self.menu_active = True
        self.adjusting_volume = False

        self.display_sucess_message = False
        self.sucess_message_text = self.font.render(
            "Sauvegarde effectuée avec succès!",
            True,
            (0, 255, 0),
        )
        self.sucess_message_duration = 3000  # en millisecondes
        self.sucess_message_start_time = 0

    def save_volume(self):
        """Enregistre la valeur du volume dans un fichier JSON"""
        with open("settings.json", "w") as f:
            json.dump({"volume": self.volume_level}, f)

    def load_volume(self):
        """Charge la valeur du volume depuis un fichier JSON"""
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                return settings.get("volume", 1.0)
        except FileNotFoundError:
            return 1.0  # Valeur par défaut si le fichier n'existe pas

    def draw(self):
        """
        QUI: Nathan Isembaert & Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Dessine le menu de pause à l'écran
        """
        # Dessiner un fond noir semi-transparent
        s = pygame.Surface(
            (self.window_width, self.window_height)
        )  # Taille de la surface
        s.set_alpha(128)  # Transparence : 0 transparent, 255 opaque
        s.fill((0, 0, 0))  # Remplir la surface en noir
        self.window.blit(s, (0, 0))  # Dessiner la surface sur la fenêtre

        # Dessiner le fond du menu avec des coins arrondis et une ombre
        pygame.draw.rect(
            self.window,
            (255, 255, 255),
            (self.menu_x, self.menu_y, self.menu_width, self.menu_height),
            border_radius=10,
        )
        pygame.draw.rect(
            self.window,
            (230, 230, 230),
            (self.menu_x, self.title_y, self.menu_width, self.title_height),
            border_radius=10,
        )

        self.window.blit(self.pause_text, self.pause_text_rect)

        # Dessiner les boutons avec des coins arrondis
        for key, button in self.buttons.items():
            pygame.draw.rect(self.window, (0, 122, 255), button, border_radius=10)
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

        if self.display_sucess_message:
            elapsed_time = pygame.time.get_ticks() - self.sucess_message_start_time
            if elapsed_time < self.sucess_message_duration:
                sucess_message_rect = self.sucess_message_text.get_rect(
                    center=(self.window_width // 2, self.menu_y + self.menu_height + 20)
                )
                self.window.blit(self.sucess_message_text, sucess_message_rect)
            else:
                self.display_sucess_message = False

        pygame.display.update()

    def handle_events(self):
        """
        QUI: Nathan Isembaert & Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Gère les événements du menu de pause
        """
        cursor_changed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for key, button in self.buttons.items():
                        if button.collidepoint(pos):
                            self.audio.musicAmbiance("clic.mp3")
                            if key == "resume":
                                return True
                            elif key == "save":
                                self.save_game()
                            elif key == "quit":
                                pygame.quit()
                                exit()
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.audio.jouerSon("menuOpen.wav")
                    return True
        return False
    
    def save_game(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Sauvegarde le jeu dans un fichier JSON
        """
        from datetime import datetime

        print("Sauvegarde du jeu!...")
        # Charger les sauvegardes existantes ou initialiser un dictionnaire vide
        try:
            with open("saves.json", "r") as f:
                currentlySaves = json.load(f)
        except FileNotFoundError:
            currentlySaves = {}

        currentDateTime = datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

        if str(self.idOfLoadedGame) in currentlySaves:
            del currentlySaves[str(self.idOfLoadedGame)]

        currentlySaves[self.idOfLoadedGame] = {
            "time": currentDateTime,
            "level": self.joueurActif.get_level,
            "player": {
                "position": {
                    "x": self.joueurActif._x/20,
                    "y": self.joueurActif._y/20,
                },
                "inventory": self.joueurActif.get_inventaire,
                "health": self.joueurActif.get_vie,
            },
        }

        # Écraser la sauvegarde idOfLoadedGame
        with open("saves.json", "w") as f:
            # afficher un message de succès
            self.display_sucess_message = True
            self.sucess_message_start_time = pygame.time.get_ticks()

            json.dump(currentlySaves, f, indent=4)

    def run(self):
        """
        QUI: Nathan Isembaert & Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Boucle principale du menu de pause
        """
        self.audio.jouerSon("menuOpen.wav")

        while self.menu_active:
            self.draw()
            if self.handle_events():
                self.menu_active = False
            pygame.time.wait(20)
