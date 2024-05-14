import pygame

class PauseMenu:
    def __init__(self, window):
        pygame.font.init()
        self.window = window
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 50)
        self.window_width, self.window_height = window.get_size()
        
        # Dimensions et positionnement du menu
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
            self.title_y + self.title_height + 260  
        ]
        
        self.buttons = {
            'resume': pygame.Rect(self.button_x, button_positions[0], self.button_width, self.button_height),
            'save': pygame.Rect(self.button_x, button_positions[1], self.button_width, self.button_height),
            'quit': pygame.Rect(self.button_x, button_positions[3], self.button_width, self.button_height)
        }
        
        self.texts = {
            'resume': self.font.render('Retour en jeu', True, (0, 0, 0)),
            'save': self.font.render('Sauvegarder la partie', True, (0, 0, 0)),
            'quit': self.font.render('Quitter le jeu', True, (0, 0, 0))
        }
        
        # Control du volume
        self.volume_label = self.font.render('Son', True, (0, 0, 0))
        self.volume_label_rect = self.volume_label.get_rect(midtop=(self.menu_x + self.menu_width // 2, button_positions[1] + 70))
        
        self.volume_rect = pygame.Rect(self.button_x, button_positions[1] + 110, self.button_width, 20)
        self.volume_level = 1.0  # Volume initial

        self.pause_text = self.title_font.render('PAUSE', True, (0, 0, 0))
        self.pause_text_rect = self.pause_text.get_rect(center=(self.menu_x + self.menu_width // 2, self.title_y + self.title_height // 2))
        
        self.menu_active = True
        self.adjusting_volume = False

    def draw(self):
        # Dessiner un fond noir semi-transparent
        s = pygame.Surface((self.window_width, self.window_height))  # Taille de la surface
        s.set_alpha(128)  # Transparence : 0 transparent, 255 opaque
        s.fill((0, 0, 0))  # Remplir la surface en noir
        self.window.blit(s, (0, 0))  # Dessiner la surface sur la fenêtre
        
        pygame.draw.rect(self.window, (255, 255, 255), (self.menu_x, self.menu_y, self.menu_width, self.menu_height), border_radius=4)
        pygame.draw.rect(self.window, (200, 200, 200), (self.menu_x, self.title_y, self.menu_width, self.title_height))
        
        self.window.blit(self.pause_text, self.pause_text_rect)
        
        for key, button in self.buttons.items():
            text_rect = self.texts[key].get_rect(center=button.center)
            self.window.blit(self.texts[key], text_rect)

        # Affichier le volume
        self.window.blit(self.volume_label, self.volume_label_rect)
        pygame.draw.rect(self.window, (200, 200, 200), self.volume_rect)
        handle_x = self.volume_rect.x + int(self.volume_level * (self.volume_rect.width - 20))
        handle_rect = pygame.Rect(handle_x, self.volume_rect.y, 20, self.volume_rect.height)
        pygame.draw.rect(self.window, (100, 100, 100), handle_rect)

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    pos = pygame.mouse.get_pos()
                    for key, button in self.buttons.items():
                        if button.collidepoint(pos):
                            if key == 'resume':
                                return True
                            elif key == 'save':
                                print("Sauvegarde du jeu...")
                            elif key == 'quit':
                                pygame.quit()
                                exit()
                    if self.volume_rect.collidepoint(pos):
                        self.adjusting_volume = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  
                    self.adjusting_volume = False
            elif event.type == pygame.MOUSEMOTION:
                if self.adjusting_volume:
                    relative_x = event.pos[0] - self.volume_rect.x
                    self.volume_level = max(0, min(1, relative_x / (self.volume_rect.width - 20)))
                    pygame.mixer.music.set_volume(self.volume_level) 
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True 
        return False

    def run(self):
        while self.menu_active:
            self.draw()
            if self.handle_events():
                self.menu_active = False
            pygame.time.wait(20)
