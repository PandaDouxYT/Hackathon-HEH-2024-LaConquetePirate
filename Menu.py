import pygame

def pause_menu(window, clock):
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 50)
    window_width, window_height = window.get_size()

    # Dimensions et positionnement du menu
    menu_width = 450
    menu_height = 400  
    menu_x = (window_width - menu_width) // 2
    menu_y = (window_height - menu_height) // 2
    
    button_width = 260
    button_height = 50
    button_x = menu_x + (menu_width - button_width) // 2
    
    title_height = 60
    title_y = menu_y + 20
    

    button_positions = [
        title_y + title_height + 20,
        title_y + title_height + 80,
        title_y + title_height + 200,  
        title_y + title_height + 260  
    ]
    
    buttons = {
        'reprendre': pygame.Rect(button_x, button_positions[0], button_width, button_height),
        'sauver': pygame.Rect(button_x, button_positions[1], button_width, button_height),
        'quitter': pygame.Rect(button_x, button_positions[3], button_width, button_height)
    }
    
    texts = {
        'reprendre': font.render('Retour en jeu', True, (0, 0, 0)),
        'sauver': font.render('Sauvegarder la partie', True, (0, 0, 0)),
        'quitter': font.render('Quitter le jeu', True, (0, 0, 0))
    }
    
    # Control du volume
    volume_label = font.render('Son', True, (0, 0, 0))
    volume_label_rect = volume_label.get_rect(midtop=(menu_x + menu_width // 2, button_positions[1] + 70))
    
    volume_rect = pygame.Rect(button_x, button_positions[1] + 110, button_width, 20)
    volume_level = 1.0  # Volume initial

    pause_text = title_font.render('PAUSE', True, (0, 0, 0))
    pause_text_rect = pause_text.get_rect(center=(menu_x + menu_width // 2, title_y + title_height // 2))
    
    menu_active = True
    adjusting_volume = False
    
    while menu_active:
        pygame.draw.rect(window, (255, 255, 255), (menu_x, menu_y, menu_width, menu_height), border_radius=4)
        pygame.draw.rect(window, (200, 200, 200), (menu_x, title_y, menu_width, title_height))
        
        window.blit(pause_text, pause_text_rect)
        
        for key, button in buttons.items():
            text_rect = texts[key].get_rect(center=button.center)
            window.blit(texts[key], text_rect)

        # Affichier le volume
        window.blit(volume_label, volume_label_rect)
        pygame.draw.rect(window, (200, 200, 200), volume_rect)
        handle_x = volume_rect.x + int(volume_level * (volume_rect.width - 20))
        handle_rect = pygame.Rect(handle_x, volume_rect.y, 20, volume_rect.height)
        pygame.draw.rect(window, (100, 100, 100), handle_rect)

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
                            if key == 'reprendre':
                                return True
                            elif key == 'sauver':
                                print("Sauvegarde du jeu...")
                            elif key == 'quitter':
                                pygame.quit()
                                exit()
                    if volume_rect.collidepoint(pos):
                        adjusting_volume = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  
                    adjusting_volume = False
            elif event.type == pygame.MOUSEMOTION:
                if adjusting_volume:
                    relative_x = event.pos[0] - volume_rect.x
                    volume_level = max(0, min(1, relative_x / (volume_rect.width - 20)))
                    pygame.mixer.music.set_volume(volume_level) 
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True 
        
        clock.tick(60)

