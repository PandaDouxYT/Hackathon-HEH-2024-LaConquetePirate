import pygame

def pause_menu(window, clock):
    pygame.font.init()
    font = pygame.font.Font(None, 36) 
    title_font = pygame.font.Font(None, 50)  
    window_width, window_height = window.get_size()

    # Dimensions et positionnement du menu
    menu_width = 450
    menu_height = 300  
    menu_x = (window_width - menu_width) // 2
    menu_y = (window_height - menu_height) // 2
    
    button_width = 260
    button_height = 50
    button_x = menu_x + (menu_width - button_width) // 2
    
    title_height = 60  
    title_y = menu_y + 20  
    
    # Ajuste la position des boutons
    button_positions = [
        title_y + title_height + 20,
        title_y + title_height + 80,
        title_y + title_height + 140
    ]
    
    buttons = {
        'resume': pygame.Rect(button_x, button_positions[0], button_width, button_height),
        'save': pygame.Rect(button_x, button_positions[1], button_width, button_height),
        'quit': pygame.Rect(button_x, button_positions[2], button_width, button_height)
    }
    
    texts = {
        'resume': font.render('Retour en jeu', True, (0, 0, 0)),
        'save': font.render('Sauvegarder la partie', True, (0, 0, 0)),
        'quit': font.render('Quitter le jeu', True, (0, 0, 0))
    }
    
    pause_text = title_font.render('PAUSE', True, (0, 0, 0))
    pause_text_rect = pause_text.get_rect(center=(menu_x + menu_width // 2, title_y + title_height // 2))
    
    menu_active = True
    while menu_active:
        pygame.draw.rect(window, (255, 255, 255), (menu_x, menu_y, menu_width, menu_height),border_radius=4)  # Rectangle blanc du menu
        pygame.draw.rect(window, (200, 200, 200), (menu_x, title_y, menu_width, title_height)) 
        
        window.blit(pause_text, pause_text_rect) 
        
        for key, button in buttons.items():
            text_rect = texts[key].get_rect(center=button.center)
            window.blit(texts[key], text_rect)  

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    pos = pygame.mouse.get_pos()
                    for key, button in buttons.items():
                        if button.collidepoint(pos):
                            if key == 'resume':
                                return True
                            elif key == 'save':
                                print("Sauvegarde du jeu...")
                            elif key == 'quit':
                                pygame.quit()
                                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True 

        clock.tick(20)
