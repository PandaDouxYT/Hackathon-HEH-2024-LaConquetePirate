import pygame

def pause_menu(window, clock):
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    window_width, window_height = window.get_size()
    
    button_width = 200
    button_height = 50
    vertical_space = 100  # Espace vertical entre les boutons
    
    buttons = {
        'resume': pygame.Rect((window_width - button_width) // 2, (window_height - 3 * button_height - 2 * vertical_space) // 2, button_width, button_height),
        'save': pygame.Rect((window_width - button_width) // 2, (window_height - button_height) // 2, button_width, button_height),
        'quit': pygame.Rect((window_width - button_width) // 2, (window_height + button_height + vertical_space) // 2, button_width, button_height)
    }
    
    texts = {
        'resume': font.render('Reprendre le Jeu', True, (255, 255, 255)),
        'save': font.render('Sauvegarder', True, (255, 255, 255)),
        'quit': font.render('Quitter le Jeu', True, (255, 255, 255))
    }
    
    menu_active = True
    while menu_active:
        window.fill((30, 30, 30))  # Fond gris foncé
        for key, button in buttons.items():
            pygame.draw.rect(window, (0, 128, 128), button)  # Dessine le bouton
            text_rect = texts[key].get_rect(center=button.center)
            window.blit(texts[key], text_rect)  # Dessine le texte

        pygame.display.update()
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Bouton gauche de la souris
                    pos = pygame.mouse.get_pos()
                    if buttons['resume'].collidepoint(pos):
                        return True
                    elif buttons['save'].collidepoint(pos):
                        print("Sauvegarde du jeu...")  # Placeholder pour la fonctionnalité de sauvegarde
                    elif buttons['quit'].collidepoint(pos):
                        pygame.quit()
                        exit()

        clock.tick(20)
