import pygame, os

class Interface:
    def __init__(self, window):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Initialisation de l'interface
        """
        self.window = window
        self.font = pygame.font.Font(None, 36)

        print("Interface initialisée")
        
    def draw(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Dessine l'interface principale du jeu
        """
        self.afficher_joueur_actif()
        self.afficher_barre_vie(50)
        self.afficher_nombre_piece()
        self.afficher_nombre_experience()

    def afficher_joueur_actif(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Affiche le joueur actif en haut à gauche de la fenêtre
        """

        # Chargement des images
        joueur1_selected_img = pygame.image.load(os.path.join("assets", "img", "afficherJoueur1_selected.png"))
        joueur2_unselected_img = pygame.image.load(os.path.join("assets", "img", "afficherJoueur2_unselected.png"))
        joueur3_unselected_img = pygame.image.load(os.path.join("assets", "img", "afficherJoueur3_unselected.png"))

        # Positionnement des images
        joueur1_selected_x = 10
        joueur1_selected_y = 10

        joueur2_unselected_x = joueur1_selected_x + joueur1_selected_img.get_width() + 10
        joueur2_unselected_y = 10

        joueur3_unselected_x = joueur2_unselected_x + joueur2_unselected_img.get_width() + 10
        joueur3_unselected_y = 10

        # Dessiner les images sur la fenêtre
        self.window.blit(joueur1_selected_img, (joueur1_selected_x, joueur1_selected_y))
        self.window.blit(joueur2_unselected_img, (joueur2_unselected_x, joueur2_unselected_y))
        self.window.blit(joueur3_unselected_img, (joueur3_unselected_x, joueur3_unselected_y))

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


    def afficher_nombre_piece(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Affiche le nombre de pièces du joueur actif
        """
        # Chargement de l'image de la pièce
        coin_img = pygame.image.load(os.path.join("assets", "img", "coin.png"))
        coin_width = coin_img.get_width()

        # Création du texte
        text = self.font.render("0", True, (255, 255, 255))
        text_width = text.get_width()
        text_height = text.get_height()

        window_width = self.window.get_width()

        # Positionnement de l'image à 10 pixels du bord droit de la fenêtre et du haut
        coin_x = window_width - coin_width - text_width - 30  # 10 pixels d'espace entre le texte et l'image + 10 du bord
        coin_y = 10

        # Positionnement du texte juste à côté de l'image
        text_x = coin_x + coin_width + 10
        text_y = coin_y + (coin_img.get_height() / 2) - (text_height / 2)  # Alignement vertical au centre de l'image

        # Dessiner l'image et le texte sur la fenêtre
        self.window.blit(coin_img, (coin_x, coin_y))
        self.window.blit(text, (text_x, text_y))

    def afficher_nombre_experience(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Affiche le nombre d'expérience du joueur actif
        """

        # Chargement de l'image de l'expérience
        xp_img = pygame.image.load(os.path.join("assets", "img", "xp.png"))
        xp_width = xp_img.get_width()

        # Création du texte
        text = self.font.render("0", True, (255, 255, 255))
        text_width = text.get_width()
        text_height = text.get_height()

        window_width = self.window.get_width()

        # Positionnement de l'image à 10 pixels du bord droit de la fenêtre et du haut
        xp_x = window_width - xp_width - text_width - 30
        xp_y = 10 + xp_img.get_height() + 20

        # Positionnement du texte juste à côté de l'image
        text_x = xp_x + xp_width + 10
        text_y = xp_y + (xp_img.get_height() / 2) - (text_height / 2)

        # Dessiner l'image et le texte sur la fenêtre
        self.window.blit(xp_img, (xp_x, xp_y))
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
        window_height = self.window.get_height()

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
