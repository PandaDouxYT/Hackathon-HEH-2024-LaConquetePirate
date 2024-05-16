import pygame
import os
import json
import time
import random
from PauseMenu import PauseMenu
from Joueur import Joueur
from Personnage import Personnage
from Ennemi import Ennemi
from Carte import Carte
from Audio import Audio

class Interface:
    def __init__(self, window, idOfLoadedGame=None):
        self.window = window
        self.font = pygame.font.Font(None, 36)
        self.idOfLoadedGame = idOfLoadedGame
        self.last_trap_time = 0

        # LE NIVEAU DE LA CARTE
        # CHANGEMENT DE CARTE NON IMPLEMENTE
        self.niveauCarte = 1

        with open("map/carte"+str(self.niveauCarte)+".json", "r") as f:
            map_data = json.load(f)

        self.audio = Audio()
        self.volume_level = self.load_volume()
        self.audio.set_global_volume(self.volume_level)
        self.audio.musicAmbiance(map_data['music'], True)
        self.audio.jouerSon("startGame.mp3")
        
        player_position = None
        
        if idOfLoadedGame:
            with open("saves.json", "r") as f:
                saves = json.load(f)
                for save_id, save_data in saves.items():
                    if save_id == str(idOfLoadedGame):
                        player_position = (save_data["player"]["position"]['x'], save_data["player"]["position"]['y'])
                        self.vieJoueur = save_data["player"]["health"]
                        break
        else:
            for element in map_data['elements']:
                if element['type'] == 'joueur':
                    player_position = element['position']
                    break

        personnage = [
            Personnage("Capitaine Melon", "longueDistance", 10),
            Personnage("Capitaine Melon", "midDistance", 15),
            Personnage("Capitaine Melon", "courteDistance", 15)
        ]
        personnageEnCours = personnage[0]
        self.joueurActif = Joueur(personnageEnCours, player_position[0] * 20, player_position[1] * 20 + 100, "")
        self.joueurActif.level = self.niveauCarte

        if not idOfLoadedGame:
            self.vieJoueur = self.joueurActif.get_vie
            if os.path.exists("saves.json"):
                with open("saves.json", "r") as f:
                    saves = json.load(f)
                    self.idOfLoadedGame = len(saves) + 1

        for element in map_data['elements']:
            if element['type'] == 'ennemi':
                ennemi_position = element['position']
                break

        self.idOfActivePlayer = "1"
        self.ennemiActif = Ennemi("Vertigo", "courteDistance", 95, 20, [], 2, ennemi_position[0]*20, ennemi_position[1]*20)
        self.pause_menu = PauseMenu(self.window, self.idOfLoadedGame, self.joueurActif)

        self.xpJoueur = self.joueurActif.get_xp
        self.pieceJoueur = self.joueurActif.get_piece

        self.keys = {'left': False, 'right': False}
        self.clock = pygame.time.Clock()
        self.background_surface = None
        self.carte = self.charger_carte()
        self.enemy_killed = False  # Track if the enemy has been killed at least once
        print("Carte chargée...")
        print("Interface initialisée")

    def save_volume(self):
        with open("settings.json", "w") as f:
            json.dump({"volume": self.volume_level}, f)

    def load_volume(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                return settings.get("volume", 1.0)
        except FileNotFoundError:
            return 1.0
    
    def charger_carte(self):
        print("Chargement de la carte...")
        mesCarte = Carte(["map/carte1.json", "map/carte2.json"], self.niveauCarte)
        mapActuelle = mesCarte.charger_carte()

        taille_case = 20

        decor_path = os.path.join(mapActuelle["decor"])
        decor_image = pygame.image.load(decor_path)
        decor_image = pygame.transform.scale(decor_image, (mapActuelle["taille"][0] * taille_case, mapActuelle["taille"][1] * taille_case))

        self.background_surface = pygame.Surface((self.window.get_width(), self.window.get_height()))
        self.background_surface.fill((73, 140, 255))
        self.background_surface.blit(decor_image, (0, self.window.get_height() - decor_image.get_height()))

        elements = []

        for element in mapActuelle["elements"]:
            element_type = element["type"]
            position = element["position"]
            taille = element["taille"]

            x = position[0] * taille_case
            y = position[1] * taille_case

            taille = (taille[0] * taille_case, taille[1] * taille_case)

            elements.append((element_type, (x, y), taille))

        return {"elements": elements}

    def draw(self):
        if self.background_surface:
            self.window.blit(self.background_surface, (0, 0))

        self.afficher_carte()

        self.afficher_joueur_actif()
        self.afficher_barre_vie(self.vieJoueur)
        self.afficher_nombre_piece(self.pieceJoueur)
        self.afficher_nombre_experience(self.xpJoueur)
        self.afficher_nombre_level(self.joueurActif.level)
        self.afficher_barre_vie_ennemi("Vertigo", 100)

        self.joueurActif.mettre_a_jour_position()
        self.ennemiActif.mettre_a_jour_position()

        self.ennemiActif.verifier_mort()

        if self.ennemiActif._vie <= 1:
            self.enemy_killed = True

        self.vieJoueur = self.ennemiActif.attaque(self.joueurActif, self.vieJoueur)
        self.ennemiActif.deplacer(self.joueurActif._x, self.joueurActif._y)

        if self.idOfLoadedGame:
            fontCredits = pygame.font.SysFont(None, 20)
            credits_surface = fontCredits.render('Vous jouez sur votre sauvegarde: #' + str(self.idOfLoadedGame), True, (255, 255, 255))
            credits_rect = credits_surface.get_rect(center=(self.window.get_width() - 140, self.window.get_height() - 20))
            self.window.blit(credits_surface, credits_rect)
        else:
            if os.path.exists("saves.json"):
                with open("saves.json", "r") as f:
                    if os.stat("saves.json").st_size == 0:
                        with open("saves.json", "w") as f:
                            json.dump({}, f)
            else:
                with open("saves.json", "w") as f:
                    json.dump({}, f)
            with open("saves.json", "r") as f:
                currentlySaves = json.load(f)
                print("Ton id de sauvegarde est: ", len(currentlySaves) + 1)
                self.idOfLoadedGame = len(currentlySaves) + 1
        
        pygame.display.update()

    def afficher_carte(self):
        elementCollision = ["mur", "sol"]

        for element_type, position, taille in self.carte["elements"]:
            if element_type in elementCollision:
                pass
            elif element_type == "piece":
                coin_img = pygame.image.load(os.path.join("assets", "img", "cle.png"))
                coin_img = pygame.transform.scale(coin_img, (taille[0], taille[1]))
                self.window.blit(coin_img, position)
            elif element_type == "piege":
                piques_img = pygame.image.load(os.path.join("assets", "img", "piques.png"))
                piques_img = pygame.transform.scale(piques_img, (taille[0], taille[1]))
                self.window.blit(piques_img, position)
            if element_type == "roche":
                pygame.draw.rect(self.window, (88, 56, 32), pygame.Rect(position, taille))
            elif element_type == "trou":
                rayon = taille[0] // 2
                pygame.draw.circle(self.window, (0, 0, 0), (position[0] + rayon, position[1] + rayon), rayon)
            elif element_type == "porte":
                taille_porte = (taille[0] // 2, taille[1] * 2)
                pygame.draw.rect(self.window, (100, 50, 0), pygame.Rect(position, taille_porte))

    def effacer_zone(self, x, y, width, height):
        self.window.fill((73, 140, 255), (x, y, width, height))
    
    def run(self):
        interface_active = True
        while interface_active:
            self.clock.tick(60)
            
            ennemi_rect = self.ennemiActif.get_rect()

            for element_type, position, taille in self.carte["elements"]:
                element_rect = pygame.Rect(position, taille)

                if element_type in ["mur"] and ennemi_rect.colliderect(element_rect):
                    if not self.ennemiActif._facing_right:
                        self.ennemiActif._x = element_rect.right
                    else:
                        self.ennemiActif._x = element_rect.left - ennemi_rect.width - 10

            player_rect = self.joueurActif.get_rect()

            for element_type, position, taille in self.carte["elements"]:
                element_rect = pygame.Rect(position, taille)

                if element_type in ["mur"] and player_rect.colliderect(element_rect):
                    if self.keys['left']:
                        self.joueurActif._x = element_rect.right
                    elif self.keys['right']:
                        self.joueurActif._x = element_rect.left - player_rect.width - 10
                if element_type in ["sol"] and player_rect.colliderect(element_rect):
                    yOfSol = element_rect.top
                    self.joueurActif._y = yOfSol
                    self.joueurActif._saut_en_cours = False
                    self.joueurActif._vitesse_actuelle_saut = self.joueurActif._vitesse_saut * self.joueurActif._hauteur_saut
                if element_type in ["roche"] and player_rect.colliderect(element_rect):
                    if player_rect.bottom <= element_rect.top + self.joueurActif._vitesse_actuelle_saut:
                        self.joueurActif._y = element_rect.top
                        self.joueurActif._saut_en_cours = False
                        self.joueurActif._vitesse_actuelle_saut = self.joueurActif._vitesse_saut * self.joueurActif._hauteur_saut
                    elif self.joueurActif._saut_en_cours and self.joueurActif._y < element_rect.bottom - 20:
                        self.joueurActif._y = element_rect.top
                        self.joueurActif._saut_en_cours = False
                        self.joueurActif._vitesse_actuelle_saut = self.joueurActif._vitesse_saut * self.joueurActif._hauteur_saut
                if element_type in ["piege"] and player_rect.colliderect(element_rect):
                    current_time = time.time()
                    if current_time - self.last_trap_time >= 1.2:
                        self.vieJoueur -= 10
                        self.last_trap_time = current_time
                        self.xpJoueur -= 1
                        self.audio.jouerSon("hurt.mp3")
                if element_type in ["piece"] and player_rect.colliderect(element_rect):
                    print("Collision avec une pièce")
                    print(self.enemy_killed)
                    if self.enemy_killed: 
                        self.pieceJoueur += random.randint(10, 25)
                        self.xpJoueur += random.randint(5, 10)

                        self.audio.jouerSon("supermariocoin.mp3")
                        self.carte["elements"].remove((element_type, position, taille))

                        
                        # TODO: FAIRE LE CHANGEMENT DE MAP ICI
                        self.niveauCarte = 2
                        
                        self.afficher_message_de_victoire()

            if self.vieJoueur <= 0:
                self.joueurActif.set_vie(0)
                print("Vous êtes mort")
                self.pause_menu.save_game()
                self.afficher_message_de_mort()
                break

            self.joueurActif.appliquerGravite(self.carte["elements"])

            self.joueurActif.verifier_collisions_fleches(self.ennemiActif)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu.run()
                    elif event.key == pygame.K_q:
                        self.keys['left'] = True
                    elif event.key == pygame.K_d:
                        self.keys['right'] = True
                    elif event.key == pygame.K_SPACE:
                        self.audio.jouerSon("jump.mp3")
                        self.joueurActif.sauter()
                    elif event.key == pygame.K_1:
                        self.joueurActif.ChangerPersonnage(1)
                        self.idOfActivePlayer = "1"
                    elif event.key == pygame.K_2:
                        self.joueurActif.ChangerPersonnage(2)
                        self.idOfActivePlayer = "2"
                    elif event.key == pygame.K_3:
                        self.joueurActif.ChangerPersonnage(3)
                        self.idOfActivePlayer = "3"
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        self.keys['left'] = False
                    elif event.key == pygame.K_d:
                        self.keys['right'] = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.joueurActif.tirer_fleche()

            if self.keys['left']:
                self.joueurActif.deplacer_gauche()
            if self.keys['right']:
                self.joueurActif.deplacer_droite()

            if self.joueurActif._saut_en_cours:
                self.joueurActif._y -= self.joueurActif._vitesse_actuelle_saut
                self.joueurActif._vitesse_actuelle_saut += self.joueurActif._gravite
            if self.joueurActif._y >= self.window.get_height():
                self.joueurActif._y = self.window.get_height()
                self.joueurActif._saut_en_cours = False
                self.joueurActif._vitesse_actuelle_saut = self.joueurActif._vitesse_saut * self.joueurActif._hauteur_saut

            self.joueurActif.appliquerGravite(self.carte["elements"])

            self.draw()

    def afficher_joueur_actif(self):
        joueur_imgs = {
            1: {
                'selected': pygame.image.load(os.path.join("assets", "img", "afficherJoueur1_selected.png")),
                'unselected': pygame.image.load(os.path.join("assets", "img", "afficherJoueur1_unselected.png"))
            },
            2: {
                'selected': pygame.image.load(os.path.join("assets", "img", "afficherJoueur2_selected.png")),
                'unselected': pygame.image.load(os.path.join("assets", "img", "afficherJoueur2_unselected.png"))
            },
            3: {
                'selected': pygame.image.load(os.path.join("assets", "img", "afficherJoueur3_selected.png")),
                'unselected': pygame.image.load(os.path.join("assets", "img", "afficherJoueur3_unselected.png"))
            }
        }
        joueur1_img = joueur_imgs[1]['selected'] if self.idOfActivePlayer == "1" else joueur_imgs[1]['unselected']
        joueur2_img = joueur_imgs[2]['selected'] if self.idOfActivePlayer == "2" else joueur_imgs[2]['unselected']
        joueur3_img = joueur_imgs[3]['selected'] if self.idOfActivePlayer == "3" else joueur_imgs[3]['unselected']

        joueur1_selected_x = 10
        joueur1_selected_y = 10

        joueur2_unselected_x = joueur1_selected_x + joueur1_img.get_width() + 10
        joueur2_unselected_y = 10

        joueur3_unselected_x = joueur2_unselected_x + joueur2_img.get_width() + 10
        joueur3_unselected_y = 10

        self.window.blit(joueur1_img, (joueur1_selected_x, joueur1_selected_y))
        self.window.blit(joueur2_img, (joueur2_unselected_x, joueur2_unselected_y))
        self.window.blit(joueur3_img, (joueur3_unselected_x, joueur3_unselected_y))

    def afficher_barre_vie(self, pourcentage):
        self.joueurActif.set_vie(self.vieJoueur)

        barre_vie_x = 10
        barre_vie_y = 180
        barre_vie_width = 455 
        barre_vie_height = 20

        remplissage_width = (pourcentage / 100) * barre_vie_width

        pygame.draw.rect(self.window, (128, 128, 128), (barre_vie_x, barre_vie_y, barre_vie_width, barre_vie_height))

        pygame.draw.rect(self.window, (0, 255, 0), (barre_vie_x, barre_vie_y, remplissage_width, barre_vie_height))

    def afficher_nombre_piece(self, nb_pieces=0):
        coin_img = pygame.image.load(os.path.join("assets", "img", "coin.png"))
        coin_width = coin_img.get_width()

        text = self.font.render(str(nb_pieces), True, (255, 255, 255))
        text_width = text.get_width()
        text_height = text.get_height()

        window_width = self.window.get_width()

        coin_x = window_width - coin_width - text_width - 30
        coin_y = 10

        text_x = coin_x + coin_width + 10
        text_y = coin_y + (coin_img.get_height() / 2) - (text_height / 2)

        self.effacer_zone(coin_x, coin_y, coin_width + text_width + 20, coin_img.get_height())

        self.window.blit(coin_img, (coin_x, coin_y))
        self.window.blit(text, (text_x, text_y))

    def afficher_nombre_level(self, level=0):
        xp_img = pygame.image.load(os.path.join("assets", "img", "level.png"))
        xp_width = xp_img.get_width()

        text = self.font.render(str(level), True, (255, 255, 255))
        text_width = text.get_width()
        text_height = text.get_height()

        window_width = self.window.get_width()

        xp_x = window_width - xp_width - text_width - 30
        xp_y = 10 + xp_img.get_height() + 20

        text_x = xp_x + xp_width + 10
        text_y = xp_y + (xp_img.get_height() / 2) - (text_height / 2)

        self.effacer_zone(xp_x, xp_y, xp_width + text_width + 20, xp_img.get_height())

        self.window.blit(xp_img, (xp_x, xp_y))
        self.window.blit(text, (text_x, text_y))

    def afficher_nombre_experience(self, xp=0):
        text = self.font.render(str(xp), True, (255, 255, 255))
        text_width = text.get_width()
        text_height = text.get_height()

        window_width = self.window.get_width()

        text_x = window_width - text_width - 20
        text_y = 105

        self.effacer_zone(text_x - 10, text_y, text_width + 20, text_height)

        self.window.blit(text, (text_x, text_y))


    def actualiser_inventaire(self, listeObjets):
        for i, objet in enumerate(listeObjets):
            objet_img = pygame.image.load(os.path.join("assets", "img", objet + ".png"))
            objet_img = pygame.transform.scale(objet_img, (45, 45))

            objet_x = 10 + i * (objet_img.get_width() + 10)
            objet_y = 220

            self.window.blit(objet_img, (objet_x, objet_y))

    def afficher_barre_vie_ennemi(self, nom_ennemi, pourcentage):
        barre_vie_height = 20
        barre_vie_width = 500
        barre_vie_y = 50

        window_width = self.window.get_width()

        barre_vie_x = (window_width - barre_vie_width) // 2

        remplissage_width = (pourcentage / 100) * barre_vie_width

        pygame.draw.rect(self.window, (128, 128, 128), (barre_vie_x, barre_vie_y, barre_vie_width, barre_vie_height))
        
        pygame.draw.rect(self.window, (0, 255, 0), (barre_vie_x, barre_vie_y, remplissage_width, barre_vie_height))
        
        font = pygame.font.Font(None, 36)
        text = font.render(nom_ennemi, True, (255, 255, 255))
        text_width = text.get_width()
        text_x = (window_width - text_width) // 2
        text_y = barre_vie_y - 30
        
        self.window.blit(text, (text_x, text_y))

    def afficher_objet(self):
        if self.__monObjet is not None:
            try:
                monObjet = self.__monObjet[0] + ".png"
                chemin_image = os.path.join("assets", "img", monObjet)

                objet_img = pygame.image.load(chemin_image)
                objet_img = pygame.transform.scale(objet_img, (200, 100))

                objet_x = 100
                objet_y = 200

                self.window.blit(objet_img, (objet_x, objet_y))
            except pygame.error as e:
                print(f"Erreur lors du chargement de l'image {chemin_image}: {e}")

    def afficher_message_de_mort(self):
        import pygame
        import time

        self.audio.stopMusic()
        self.audio.set_global_volume(1.0)
        time.sleep(1)
        self.audio.jouerSon("death.mp3")

        overlay = pygame.Surface((self.window.get_width(), self.window.get_height()))
        overlay.fill((0, 0, 0))
        self.window.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 48)
        message = font.render("Cette partie c'est fini pour vous !", True, (255, 255, 255))
        message_rect = message.get_rect(center=(self.window.get_width() / 2, self.window.get_height() / 2))
        self.window.blit(message, message_rect)

        small_font = pygame.font.Font(None, 32)
        sub_message = small_font.render("Vous êtes mort !", True, (255, 255, 255))
        sub_message_rect = sub_message.get_rect(center=(self.window.get_width() / 2, self.window.get_height() / 2 + 50))
        self.window.blit(sub_message, sub_message_rect)

        button_width, button_height = 200, 50
        button_color_start = (255, 255, 255)
        button_color_end = (200, 200, 200)
        button_position = (
            (self.window.get_width() - button_width) / 2,
            self.window.get_height() / 2 + 150
        )
        button_rect = pygame.Rect(button_position[0], button_position[1], button_width, button_height)

        for i in range(button_height):
            color = [
                button_color_start[j] + (button_color_end[j] - button_color_start[j]) * (i / button_height)
                for j in range(3)
            ]
            pygame.draw.line(self.window, color, (button_rect.left, button_rect.top + i), (button_rect.right, button_rect.top + i))

        pygame.draw.rect(self.window, button_color_start, button_rect, border_radius=10)

        button_text = small_font.render("Quitter", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.window.blit(button_text, button_text_rect)

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button_rect.collidepoint(mouse_pos):
                        waiting = False
                        pygame.quit()
                        exit()

    def afficher_message_de_victoire(self):
        self.audio.stopMusic()
        self.audio.set_global_volume(1.0)
        time.sleep(1)
        self.audio.jouerSon("victory.mp3")

        overlay = pygame.Surface((self.window.get_width(), self.window.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        self.window.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 48)
        message = font.render("C'est gagné !", True, (255, 215, 0))
        message_rect = message.get_rect(center=(self.window.get_width() / 2, self.window.get_height() / 2))
        self.window.blit(message, message_rect)

        small_font = pygame.font.Font(None, 32)
        sub_message = small_font.render("Vous avez réussi à tuer tous les boss !", True, (255, 215, 0))
        sub_message_rect = sub_message.get_rect(center=(self.window.get_width() / 2, self.window.get_height() / 2 + 50))
        self.window.blit(sub_message, sub_message_rect)

        extra_message = small_font.render("À vous l'or et les bateaux en tous genres !", True, (255, 215, 0))
        extra_message_rect = extra_message.get_rect(center=(self.window.get_width() / 2, self.window.get_height() / 2 + 100))
        self.window.blit(extra_message, extra_message_rect)

        button_width, button_height = 200, 50
        button_color_start = (255, 255, 255)
        button_color_end = (200, 200, 200)
        button_position = (
            (self.window.get_width() - button_width) / 2,
            self.window.get_height() / 2 + 200
        )
        button_rect = pygame.Rect(button_position[0], button_position[1], button_width, button_height)

        for i in range(button_height):
            color = [
                button_color_start[j] + (button_color_end[j] - button_color_start[j]) * (i / button_height)
                for j in range(3)
            ]
            pygame.draw.line(self.window, color, (button_rect.left, button_rect.top + i), (button_rect.right, button_rect.top + i))

        pygame.draw.rect(self.window, button_color_start, button_rect, border_radius=10)

        button_text = small_font.render("Quitter", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.window.blit(button_text, button_text_rect)

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button_rect.collidepoint(mouse_pos):
                        waiting = False
                        pygame.quit()
                        exit()
