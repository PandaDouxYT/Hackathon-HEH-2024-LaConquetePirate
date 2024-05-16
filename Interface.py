import pygame
import os
import json
import time  # Import the time module
from PauseMenu import PauseMenu
from Joueur import Joueur
from Personnage import Personnage
from Ennemi import Ennemi
from Carte import Carte
from Audio import Audio

class Interface:
    def __init__(self, window, idOfLoadedGame=None):
        """
        QUI: Anthony VERGEYLEN & Guillaume DUCHESNE
        QUAND: 16-05-2024
        QUOI: Initialisation de l'interface du jeu
        """
        self.window = window
        self.font = pygame.font.Font(None, 36)
        self.idOfLoadedGame = idOfLoadedGame
        self.last_trap_time = 0  # Initialize the last trap interaction time to 0

        self.niveauCarte = 2

        with open("map/carte"+str(self.niveauCarte)+".json", "r") as f:
            map_data = json.load(f)

        self.audio = Audio()
        self.volume_level = self.load_volume()  # Charger le volume initial
        self.audio.set_global_volume(self.volume_level)
        self.audio.musicAmbiance(map_data['music'], True)
        self.audio.jouerSon("startGame.mp3")

        # Initialize player's position
        player_position = None

        # Iterate through elements to find the player
        for element in map_data['elements']:
            if element['type'] == 'joueur':
                player_position = element['position']
                break

        for element in map_data['elements']:
            if element['type'] == 'ennemi':
                ennemi_position = element['position']
                break

        personnage = [
            Personnage("Capitaine Melon", "longueDistance", 10),
            Personnage("Capitaine Melon", "midDistance", 15),
            Personnage("Capitaine Melon", "courteDistance", 15)
        ]
        personnageEnCours = personnage[0]
        self.joueurActif = Joueur(personnageEnCours, player_position[0] * 20, player_position[1] * 20 + 100, "")
        
        self.idOfActivePlayer = "1"
        self.ennemiActif = Ennemi("Vertigo", "courteDistance", 95, 20, [], 2, ennemi_position[0]*20, ennemi_position[1]*20)

        self.vieJoueur = self.joueurActif.get_vie
        print("Vie l: ", self.vieJoueur)
        self.xpJoueur = self.joueurActif.get_xp
        self.pieceJoueur = self.joueurActif.get_piece
        self.levelJoueur = self.joueurActif.get_level

        self.keys = {'left': False, 'right': False}
        self.clock = pygame.time.Clock()
        self.background_surface = None
        self.carte = self.charger_carte()
        print("Carte chargée...")
        print(self.carte)
        print("Interface initialisée")

    def save_volume(self):
        """
        QUI: Anthony VERGEYLEN & Guillaume DUCHESNE
        QUAND: 16-05-2024
        QUOI: Sauvegarde la valeur du volume dans un fichier JSON 
        """
        with open("settings.json", "w") as f:
            json.dump({"volume": self.volume_level}, f)

    def load_volume(self):
        """
        QUI: Anthony VERGEYLEN & Guillaume DUCHESNE
        QUAND: 16-05-2024
        QUOI: Charge la valeur du volume depuis un fichier JSON
        """
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                return settings.get("volume", 1.0)
        except FileNotFoundError:
            return 1.0  # Valeur par défaut si le fichier n'existe pas
    
    def charger_carte(self):
        """
        QUI: Anthony VERGEYLEN & Guillaume DUCHESNE
        QUAND: 16-05-2024
        QUOI: Charge la carte du jeu depuis un fichier JSON
        """

        print("Chargement de la carte...")
        mesCarte = Carte(["map/carte1.json", "map/carte2.json"], self.niveauCarte)
        mapActuelle = mesCarte.charger_carte()
        print("Carte chargée...")

        taille_case = 20  # Taille d'une case en pixels

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
        """
        QUI: Anthony VERGEYLEN & Guillaume DUCHESNE
        QUAND: 16-05-2024
        QUOI: Dessine l'interface du jeu
        """
        if self.background_surface:
            self.window.blit(self.background_surface, (0, 0))

        self.afficher_carte()

        self.afficher_joueur_actif()
        self.afficher_barre_vie(self.vieJoueur)
        self.afficher_nombre_piece(self.pieceJoueur)
        self.afficher_nombre_experience(self.xpJoueur)
        self.afficher_nombre_level(self.levelJoueur)
        self.afficher_barre_vie_ennemi("Vertigo", 100)

        # Affichage du personnage joueur
        self.joueurActif.mettre_a_jour_position()

        # Affichage de l'ennemi
        self.ennemiActif.mettre_a_jour_position()

        # print("Vie ennemi: ", self.ennemiActif._vie)

        self.ennemiActif.verifier_mort()

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
                self.idOfLoadedGame = len(currentlySaves) + 1
        
        pygame.display.update()

    def afficher_carte(self):
        """
        QUI: Anthony VERGEYLEN & Guillaume DUCHESNE
        QUAND: 16-05-2024
        QUOI: Affiche la carte du jeu
        """
        elementCollision = ["mur", "sol"]

        for element_type, position, taille in self.carte["elements"]:
            if element_type in elementCollision:
                # if element_type == "mur":
                #     pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(position, taille))
                # elif element_type == "sol":
                #     pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(position, taille))
                pass
            elif element_type == "piece":
                # draw coin.png at position
                coin_img = pygame.image.load(os.path.join("assets", "img", "coin.png"))
                coin_img = pygame.transform.scale(coin_img, (taille[0], taille[1]))
                self.window.blit(coin_img, position)
            elif element_type == "piege":
                rayon = taille[0] // 2
                # draw piques.png at position
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
        """
        QUI: Anthony VERGEYLEN & Guillaume DUCHESNE
        QUAND: 16-05-2024
        QUOI: Efface une zone de la fenêtre
        # x: position x de la zone à effacer
        # y: position y de la zone à effacer
        # width: largeur de la zone à effacer
        # height: hauteur de la zone à effacer
        """
        self.window.fill((73, 140, 255), (x, y, width, height))
    
    def run(self):
        """
        QUI: Anthony VERGEYLEN & Guillaume DUCHESNE
        QUAND: 16-05-2024
        QUOI: Lance l'interface du jeu
        """
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
                    if current_time - self.last_trap_time >= 1.2:  # Check if 1.2 seconds have passed
                        self.vieJoueur -= 10

                        self.last_trap_time = current_time
                        self.xpJoueur -= 1
                        self.audio.jouerSon("hurt.mp3")
                if element_type in ["piece"] and player_rect.colliderect(element_rect):
                    self.pieceJoueur += 1
                    self.audio.jouerSon("supermariocoin.mp3")
                    self.carte["elements"].remove((element_type, position, taille))

            if self.vieJoueur <= 0:
                print("Vous êtes mort")
                self.afficher_message_de_mort()
                break

            self.joueurActif.appliquerGravite(self.carte["elements"])

            self.joueurActif.verifier_collisions_fleches(self.ennemiActif)  # Ajoutez cet appel

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu = PauseMenu(self.window, self.idOfLoadedGame, self.joueurActif)
                        pause_menu.run()
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
                    if event.button == 3:  # Right-click event
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
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Affiche le joueur actif en haut à gauche de la fenêtre
        """
        # Définir les chemins des images
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

        # Positionnement des images
        joueur1_selected_x = 10
        joueur1_selected_y = 10

        joueur2_unselected_x = joueur1_selected_x + joueur1_img.get_width() + 10
        joueur2_unselected_y = 10

        joueur3_unselected_x = joueur2_unselected_x + joueur2_img.get_width() + 10
        joueur3_unselected_y = 10

        # Dessiner les images sur la fenêtre
        self.window.blit(joueur1_img, (joueur1_selected_x, joueur1_selected_y))
        self.window.blit(joueur2_img, (joueur2_unselected_x, joueur2_unselected_y))
        self.window.blit(joueur3_img, (joueur3_unselected_x, joueur3_unselected_y))

    def afficher_barre_vie(self, pourcentage):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Affiche la barre de vie du joueur actif
        # pourcentage: pourcentage de vie restante du joueur actif (eg. 50 pour 50% de vie restante)
        """

        barre_vie_x = 10
        barre_vie_y = 180
        barre_vie_width = 455 
        barre_vie_height = 20

        # Calculer la largeur de la partie remplie de la barre de vie
        remplissage_width = (pourcentage / 100) * barre_vie_width

        # Dessiner le fond de la barre de vie (gris pour la partie non remplie)
        pygame.draw.rect(self.window, (128, 128, 128), (barre_vie_x, barre_vie_y, barre_vie_width, barre_vie_height))

        # Dessiner la partie remplie de la barre de vie (verte)
        pygame.draw.rect(self.window, (0, 255, 0), (barre_vie_x, barre_vie_y, remplissage_width, barre_vie_height))

    def afficher_nombre_piece(self, nb_pieces=0):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Affiche le nombre de pièces du joueur actif
        # nb_pieces: nombre de pièces du joueur actif
        """
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

        # Effacer la zone avant de redessiner
        self.effacer_zone(coin_x, coin_y, coin_width + text_width + 20, coin_img.get_height())

        self.window.blit(coin_img, (coin_x, coin_y))
        self.window.blit(text, (text_x, text_y))

    def afficher_nombre_level(self, level=0):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Affiche le niveau du joueur actif
        # level: niveau du joueur actif
        """
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

        # Effacer la zone avant de redessiner
        self.effacer_zone(xp_x, xp_y, xp_width + text_width + 20, xp_img.get_height())

        self.window.blit(xp_img, (xp_x, xp_y))
        self.window.blit(text, (text_x, text_y))

    def afficher_nombre_experience(self, xp=0):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Affiche le nombre d'expérience du joueur actif
        # xp: nombre d'expérience du joueur actif
        """
        text = self.font.render(str(xp), True, (255, 255, 255))
        text_width = text.get_width()
        text_height = text.get_height()

        window_width = self.window.get_width()

        text_x = window_width - text_width - 20
        text_y = 105

        # Effacer la zone avant de redessiner
        self.effacer_zone(text_x - 10, text_y, text_width + 20, text_height)

        self.window.blit(text, (text_x, text_y))


    def actualiser_inventaire(self, listeObjets):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Actualise l'inventaire du joueur actif
        # listeObjets: liste des objets à afficher dans l'inventaire (eg. ["chapeau", "cle", "coeur"])
        """
        for i, objet in enumerate(listeObjets):
            # Chargement de l'image de l'objet
            objet_img = pygame.image.load(os.path.join("assets", "img", objet + ".png"))

            # width to 20px and height to 20px
            objet_img = pygame.transform.scale(objet_img, (45, 45))

            # Positionnement de l'image
            objet_x = 10 + i * (objet_img.get_width() + 10)
            objet_y = 220

            # Dessiner l'image sur la fenêtre
            self.window.blit(objet_img, (objet_x, objet_y))

    def afficher_barre_vie_ennemi(self, nom_ennemi, pourcentage):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Affiche la barre de vie de l'ennemi
        # nom_ennemi: nom de l'ennemi à afficher (eg. "Goblin")
        # pourcentage: pourcentage de vie restante de l'ennemi (eg. 50 pour 50% de vie restante)
        """

        barre_vie_height = 20
        barre_vie_width = 500
        barre_vie_y = 50  # Définit la position verticale en haut avec un peu d'espace

        window_width = self.window.get_width()

        # Centrer la barre de vie horizontalement
        barre_vie_x = (window_width - barre_vie_width) // 2

        # Calculer la largeur de la partie remplie de la barre de vie
        remplissage_width = (pourcentage / 100) * barre_vie_width

        # Dessiner le fond de la barre de vie (gris)
        pygame.draw.rect(self.window, (128, 128, 128), (barre_vie_x, barre_vie_y, barre_vie_width, barre_vie_height))
        
        # Dessiner la partie remplie de la barre de vie (verte)
        pygame.draw.rect(self.window, (0, 255, 0), (barre_vie_x, barre_vie_y, remplissage_width, barre_vie_height))
        
        # Créer et positionner le texte du nom de l'ennemi
        font = pygame.font.Font(None, 36)
        text = font.render(nom_ennemi, True, (255, 255, 255))
        text_width = text.get_width()
        text_x = (window_width - text_width) // 2
        text_y = barre_vie_y - 30  # Positionner le texte au-dessus de la barre de vie
        
        # Afficher le nom de l'ennemi
        self.window.blit(text, (text_x, text_y))

    def afficher_message_de_mort(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Affiche un message de mort et attend une entrée de l'utilisateur pour quitter le jeu
        """

        # couper la musique 
        self.audio.stopMusic()
        # mettre le son a fond
        self.audio.set_global_volume(1.0)
        # wait 400 ms
        time.sleep(1)
        self.audio.jouerSon("death.mp3")

        # Draw a semi-transparent overlay
        overlay = pygame.Surface((self.window.get_width(), self.window.get_height()))
        overlay.set_alpha(200)  # Set transparency level
        overlay.fill((0, 0, 0))  # Dark gray overlay
        self.window.blit(overlay, (0, 0))

        # Use a large, modern font
        font = pygame.font.Font(None, 74)
        message = font.render("Vous êtes mort", True, (255, 255, 255))  # Render the message in white

        # Add a shadow effect to the text
        shadow = font.render("Vous êtes mort", True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(self.window.get_width() / 2 + 2, self.window.get_height() / 2 + 2))
        self.window.blit(shadow, shadow_rect)  # Blit shadow slightly offset

        text_rect = message.get_rect(center=(self.window.get_width() / 2, self.window.get_height() / 2))
        self.window.blit(message, text_rect)  # Blit the message to the center of the window

        # Render a "Press any key to exit" message
        small_font = pygame.font.Font(None, 32)
        sub_message = small_font.render("Appuyez sur une touche pour quitter", True, (255, 255, 255))
        sub_message_rect = sub_message.get_rect(center=(self.window.get_width() / 2, self.window.get_height() / 2 + 100))
        self.window.blit(sub_message, sub_message_rect)

        pygame.display.update()  # Update the display

        # Wait for user input to exit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    pygame.quit()
                    exit()
