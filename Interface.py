import pygame
import os
import json
from PauseMenu import PauseMenu
from Joueur import Joueur
from Personnage import Personnage
from Ennemi import Ennemi
from Carte import Carte

class Interface:
    def __init__(self, window, idOfLoadedGame=None):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Initialisation de l'interface
        """
        self.window = window
        self.font = pygame.font.Font(None, 36)
        self.idOfLoadedGame = idOfLoadedGame
        

        with open("map/carte1.json", "r") as f:
            map_data = json.load(f)

        # Initialize player's position
        player_position = None

        # Iterate through elements to find the player
        for element in map_data['elements']:
            if element['type'] == 'joueur':
                player_position = element['position']
                break

        # Output the player's position
        if player_position:
            print(f"Player's position: x = {player_position[0]}, y = {player_position[1]}")
        else:
            print("Player not found in the map.")

        personnage = Personnage("Capitaine Melon")
        self.joueurActif = Joueur(personnage, player_position[0]*20, player_position[1]*20)
        self.idOfActivePlayer = "1"
        self.ennemiActif = Ennemi("Goblin", 100, 20, [100, 200], [], 1)

        self.vieJoueur = self.joueurActif.get_vie
        self.xpJoueur = self.joueurActif.get_xp
        self.pieceJoueur = self.joueurActif.get_piece
        self.levelJoueur = self.joueurActif.get_level

        # Suivre l'état des touches
        self.keys = {'left': False, 'right': False}

        # Gestionnaire de temps pour contrôler le taux de rafraîchissement
        self.clock = pygame.time.Clock()

        # Charger la carte et les images une fois
        self.background_surface = None
        self.carte = self.charger_carte()

        print("Interface initialisée")

    def charger_carte(self):
        print("Chargement de la carte...")
        mesCarte = Carte(["map/carte1.json", "map/carte2.json"], 1)
        mapActuelle = mesCarte.charger_carte()
        print("Carte chargée...")

        taille_case = 20  # Taille d'une case en pixels

        # Charger le décor
        decor_path = os.path.join(mapActuelle["decor"])
        decor_image = pygame.image.load(decor_path)
        decor_image = pygame.transform.scale(decor_image, (mapActuelle["taille"][0] * taille_case, mapActuelle["taille"][1] * taille_case))

        # Créer une surface de fond
        self.background_surface = pygame.Surface((self.window.get_width(), self.window.get_height()))
        self.background_surface.fill((73, 140, 255))
        self.background_surface.blit(decor_image, (0, self.window.get_height() - decor_image.get_height()))

        # Pré-calculer les positions et tailles des éléments
        elements = []
        elementCollision = ["mur", "sol"]
        for element in mapActuelle["elements"]:
            position = (element["position"][0] * taille_case, self.window.get_height() - element["position"][1] * taille_case)
            taille = (element["taille"][0] * taille_case, element["taille"][1] * taille_case)
            position = (position[0], position[1] - taille[1])
            elements.append((element["type"], position, taille))

        return {"elements": elements}

    def draw(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Dessine l'interface principale du jeu
        """

        if self.background_surface:
            self.window.blit(self.background_surface, (0, 0))

        self.afficher_carte()

        self.afficher_joueur_actif()
        self.afficher_barre_vie(self.vieJoueur)
        self.afficher_nombre_piece(self.pieceJoueur)
        self.afficher_nombre_experience(self.xpJoueur)
        self.afficher_nombre_level(self.levelJoueur)
        self.afficher_ennemi()

        self.joueurActif.mettre_a_jour_position()  # Mise à jour de la position du joueur

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
        print("Affichage de la carte...")

        elementCollision = ["mur", "sol"]

        # Dessiner les éléments de la carte
        for element_type, position, taille in self.carte["elements"]:
            if element_type in elementCollision:
                pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(position, taille))
            elif element_type == "trou":
                rayon = taille[0] // 2
                pygame.draw.circle(self.window, (0, 0, 0), (position[0] + rayon, position[1] + rayon), rayon)
            elif element_type == "porte":
                taille_porte = (taille[0] // 2, taille[1] * 2)
                pygame.draw.rect(self.window, (100, 50, 0), pygame.Rect(position, taille_porte))
            elif element_type == "ennemi":
                pygame.draw.rect(self.window, (255, 0, 0), pygame.Rect(position, taille))
            # elif element_type == "joueur":
            #     pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(position, taille))

    def effacer_zone(self, x, y, width, height):
        """
        Efface la zone spécifiée en la remplissant avec la couleur de fond de la fenêtre.
        """
        self.window.fill((73, 140, 255), (x, y, width, height))
    
    def run(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Boucle principale de l'interface du jeu
        """
        interface_active = True
        while interface_active:
            self.clock.tick(60)  # Assure un taux de rafraîchissement de 60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu = PauseMenu(self.window, self.idOfLoadedGame, self.joueurActif)
                        pause_menu.run()
                    elif event.key == pygame.K_q:  # Déplacer à gauche
                        self.keys['left'] = True
                    elif event.key == pygame.K_d:  # Déplacer à droite
                        self.keys['right'] = True
                    elif event.key == pygame.K_SPACE:  # Déclencher le saut
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
                

            if self.keys['left']:
                self.joueurActif.deplacer_gauche()
            if self.keys['right']:
                self.joueurActif.deplacer_droite()
            
            # Gestion du saut
            if self.joueurActif._saut_en_cours:
                self.joueurActif._y -= self.joueurActif._vitesse_actuelle_saut
                self.joueurActif._vitesse_actuelle_saut += self.joueurActif._gravite
                if self.joueurActif._y <= 0:  # Supposons que la position y=0 est le sol
                    self.joueurActif._y = 0
                    self.joueurActif._saut_en_cours = False
                    self.joueurActif._vitesse_actuelle_saut = self.joueurActif._vitesse_saut * self.joueurActif._hauteur_saut

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
        Affiche le nombre de pièces du joueur actif.
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
        Affiche le niveau du joueur actif.
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
        Affiche le nombre d'expérience du joueur actif.
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
        
    def afficher_ennemi(self):
        # Charge l'image de l'ennemi
        image_path = f'assets/img/en1.gif'
        ennemi_image = pygame.image.load(image_path)
        ennemi_image = pygame.transform.scale(ennemi_image, (90, 150))

        # Position de l'image de l'ennemi
        self.window.blit(ennemi_image, (self.ennemiActif._position[0], self.ennemiActif._position[1]))