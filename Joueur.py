import pygame

class Joueur:
    def __init__(self, personnage, xJoueur, yJoueur, inventaire=[], xp=10, niveau=0, piece=0):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Constructeur de la classe Joueur

        Arguments:
        - xJoueur: int (position x du joueur)
        - yJoueur: int (position y du joueur)
        - inventaire: list (liste des objets possédés par le joueur)
        - xp: int (points d'expérience du joueur)
        - niveau: int (niveau du joueur)
        - piece: int (argent du joueur)

        Retourne:
        - Pas de retour

        """
        self._vie = 100
        self._inventaire = inventaire
        self._niveau = niveau
        self._xp = xp
        self._piece = piece
        self._hauteur_saut = 1.0
        self._personnage = personnage

        self._saut_en_cours = False
        self._vitesse_saut = 15  # vitesse initiale du saut (négative pour aller vers le haut)
        self._gravite = -1  # gravité affectant le saut
        self._vitesse_actuelle_saut = self._vitesse_saut
        
        # Load character sprites for animation
        self._idle_image = pygame.image.load("assets/img/character1idle.png")
        self._move_images = [
            pygame.image.load(f"assets/img/character1move{i}.png") for i in range(1, 5)
        ]
        
        # Resize character sprites
        self._current_image = self.resize_image(self._idle_image)
        self._move_images = [self.resize_image(image) for image in self._move_images]
        self._character_height = self._current_image.get_height()

        self._animation_index = 0
        self._animation_time = 0
        self._animation_delay = 90  # Delay in milliseconds

        self._facing_right = True  # Indicates the direction the character is facing

        self.width = 100
        self.height = 90

        self._x = xJoueur
        self._y = yJoueur

        self.window = pygame.display.get_surface()

        # Arrow properties
        self._arrow_speed = 15
        self._arrows = []
        self._last_shot_time = 0  # Time of the last shot
        self._shot_cooldown = 500  # Cooldown time in milliseconds

        # Display character at initial position
        self.afficherPersonnage(self._x, self._y)

    def resize_image(self, image):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Redimensionne une image pour qu'elle ait une largeur de 100 pixels

        Arguments:
        - image: pygame.Surface (image à redimensionner)

        Retourne:
        - pygame.Surface (image redimensionnée)

        """
        new_width = 100
        original_width, original_height = image.get_size()
        new_height = int((new_width / original_width) * original_height)
        return pygame.transform.scale(image, (new_width, new_height))
    
    def get_rect(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Retourne le rectangle de collision du joueur

        Arguments:
        - Pas d'arguments

        Retourne:
        - pygame.Rect (rectangle de collision du joueur)

        """
        return self.rect
    
    def afficherPersonnage(self, x, y):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Affiche le personnage à la position (x, y) et met à jour le rectangle de collision

        Arguments:
        - x: int (position x du joueur)
        - y: int (position y du joueur)

        Retourne:
        - Pas de retour

        """
        adjusted_y = y - self._character_height
        self.window.blit(self._current_image, (x, adjusted_y))

        self.rect = pygame.Rect(x, adjusted_y, self.width, self._character_height).inflate(-20, 5)
        self.rectDisplay = pygame.draw.rect(self.window, (255, 0, 0), (self.rect), 1)

    def mettre_a_jour_position(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Met à jour la position du joueur et affiche le personnage

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        self.afficherPersonnage(self._x, self._y)
        self.mettre_a_jour_fleches()

    def sauter(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Fait sauter le joueur

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        if not self._saut_en_cours:  # Vérifiez si le joueur n'est pas déjà en train de sauter
            self._saut_en_cours = True
            self._vitesse_actuelle_saut = self._vitesse_saut * self._hauteur_saut

    def tirer_fleche(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Fait tirer une flèche au joueur

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        current_time = pygame.time.get_ticks()
        if current_time - self._last_shot_time >= self._shot_cooldown:
            direction = 1 if self._facing_right else -1
            fleche_position = (self._x + (self.width if self._facing_right else -12), self._y - self._character_height // 2 + 10)  # Adjusted position
            self._arrows.append({'position': fleche_position, 'direction': direction})
            self._last_shot_time = current_time  # Update the time of the last shot

    def mettre_a_jour_fleches(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Met à jour la position des flèches et les affiche

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        for fleche in self._arrows:
            fleche['position'] = (fleche['position'][0] + fleche['direction'] * self._arrow_speed, fleche['position'][1])
            self.afficher_fleche(fleche['position'])
        self._arrows = [fleche for fleche in self._arrows if 0 < fleche['position'][0] < self.window.get_width()]

    def afficher_fleche(self, position):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Affiche une flèche à la position donnée

        Arguments:
        - position: tuple (position de la flèche)

        Retourne:
        - Pas de retour

        """
        fleche_image = pygame.image.load("assets/img/arrow.png")
        fleche_image = pygame.transform.scale(fleche_image, (12, 12))
        self.window.blit(fleche_image, position)

    @property
    def get_position(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Retourne la position du joueur

        Arguments:
        - Pas d'arguments

        Retourne:
        - tuple (position x, position y)

        """
        return self._personnage.get_position

    @property
    def level(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Retourne le niveau du joueur

        Arguments:
        - Pas d'arguments

        Retourne:
        - int (niveau du joueur)

        """
        return self._niveau
    
    @level.setter
    def level(self, newLevel):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Retourne le niveau du joueur

        Arguments:
        - newLevel: int (nouveau niveau du joueur)

        Retourne:
        - int (niveau du joueur)

        """
        self._niveau = newLevel
        return self._niveau

    @property
    def get_vie(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Retourne le niveau du joueur

        Arguments:
        - Pas d'arguments

        Retourne:
        - int (niveau du joueur)

        """
        return self._vie

    def set_vie(self, newLife):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Défini la vie du joueur

        Arguments:
        - newLife: int (nouvelle vie du joueur)

        Retourne:
        - int (vie du joueur)

        """
        self._vie = newLife
        return self._vie

    @property
    def get_xp(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Retourne l'expérience du joueur

        Arguments:
        - Pas d'arguments

        Retourne:
        - int (expérience du joueur)

        """
        return self._xp
    
    @property
    def get_piece(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Retourne les pieces du joueur

        Arguments:
        - Pas d'arguments

        Retourne:
        - int (pieces du joueur)

        """
        return self._piece

    @property
    def get_inventaire(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Retourne l'inventaire du joueur

        Arguments:
        - Pas d'arguments

        Retourne:
        - list (inventaire du joueur)

        """
        return self._inventaire
    
    @property
    def get_x_y(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Retourne la position du joueur

        Arguments:
        - Pas d'arguments

        Retourne:
        - tuple (position x, position y)

        """
        return self._x, self._y


    @property
    def hauteur_saut(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Retourne la hauteur de saut du joueur

        Arguments:
        - Pas d'arguments

        Retourne:
        - float (hauteur de saut du joueur)

        """
        return self._hauteur_saut

    @hauteur_saut.setter
    def hauteur_saut(self, valeur):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Défini la hauteur de saut du joueur

        Arguments:
        - valeur: float (nouvelle hauteur de saut du joueur)

        Retourne:
        - Pas de retour

        """
        self._hauteur_saut = valeur

    def RecupererObject(self, objet):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Permet au joueur de récupérer un objet

        Arguments:
        - objet: string (nom de l'objet à récupérer)

        Retourne:
        - Pas de retour

        """
        if(objet not in self._inventaire):
            self._inventaire.append(objet)
        else:
            print("Vous possedez déjà cette objet")

    def modifier_saut(self, multiplicateur):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Modifie la hauteur de saut du joueur

        Arguments:
        - multiplicateur: float (valeur par laquelle multiplier la hauteur de saut)

        Retourne:
        - Pas de retour

        """
        self._hauteur_saut *= multiplicateur
        print(f"Hauteur de saut modifiée à: {self._hauteur_saut}")

    def AjouterNiveau(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Ajoute un niveau au joueur

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        if(self._xp > 100):
            self._niveau += 1
            self._xp = 0        

    def verifier_collisions_fleches(self, ennemi):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Vérifie si une flèche touche un ennemi et l'attaque si c'est le cas

        Arguments:
        - ennemi: Ennemi (ennemi à attaquer)

        Retourne:
        - Pas de retour

        """
        for fleche in self._arrows:
            fleche_rect = pygame.Rect(fleche['position'][0], fleche['position'][1], 12, 12)
            if fleche_rect.colliderect(ennemi.get_rect()):
                self._arrows.remove(fleche)
                self.Attaquer(ennemi)


    def Attaquer(self, ennemi):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Vérifie si une flèche touche un ennemi et l'attaque si c'est le cas

        Arguments:
        - ennemi: Ennemi (ennemi à attaquer)

        Retourne:
        - Pas de retour

        """
        distance = abs(ennemi.get_x_y[0] - self._x)
        if self._personnage._type == "longueDistance":
            if distance >= 10:
                ennemi._vie -= self._personnage._degats
        elif self._personnage._type == "midDistance":
            if 5 <= distance < 10:
                ennemi._vie -= self._personnage._degats
        elif self._personnage._type == "courteDistance":
            if distance < 5:
                ennemi._vie -= self._personnage._degats

    def ChangerPersonnage(self, personnage_id):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Change le personnage du joueur

        Arguments:
        - personnage_id: int (identifiant du personnage)

        Retourne:
        - Pas de retour

        """
        # Load new character sprites for animation
        self._idle_image = pygame.image.load(f"assets/img/character{personnage_id}idle.png")
        self._move_images = [
            pygame.image.load(f"assets/img/character{personnage_id}move{i}.png") for i in range(1, 6)
        ]

        # Resize character sprites
        self._current_image = self.resize_image(self._idle_image)
        self._move_images = [self.resize_image(image) for image in self._move_images]
        self._character_height = self._current_image.get_height()

        # Reset animation index and time
        self._animation_index = 0
        self._animation_time = 0

        # Ensure the character faces the correct direction
        if not self._facing_right:
            self._current_image = pygame.transform.flip(self._current_image, True, False)
            self._move_images = [pygame.transform.flip(image, True, False) for image in self._move_images]

    def deplacer_gauche(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Déplace le joueur de 5 pixels à gauche

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        self._x -= 5  # Déplace le joueur de 5 pixels à gauche
        self.afficherPersonnage(self._x, self.window.get_height() - self._y)
        
        if self._facing_right:
            self.inverser_direction()
        self.animer_marche()

    def deplacer_droite(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Déplace le joueur de 5 pixels à droite

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        self._x += 5  # Déplace le joueur de 5 pixels à droite
        self.afficherPersonnage(self._x, self.window.get_height() - self._y)
        
        if not self._facing_right:
            self.inverser_direction()
        self.animer_marche()

    def inverser_direction(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Inverse la direction du personnage

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        self._facing_right = not self._facing_right
        self._current_image = pygame.transform.flip(self._current_image, True, False)
        self._move_images = [pygame.transform.flip(image, True, False) for image in self._move_images]

    def animer_marche(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Anime le personnage en marche

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        current_time = pygame.time.get_ticks()
        if current_time - self._animation_time > self._animation_delay:
            self._animation_index = (self._animation_index + 1) % len(self._move_images)
            self._current_image = self._move_images[self._animation_index]
            self._animation_time = current_time

    def appliquerGravite(self, elements):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Applique la gravité au joueur

        Arguments:
        - elements: list (liste des éléments du jeu)

        Retourne:
        - Pas de retour

        """
        # Appliquer la gravité si le joueur n'est pas en train de sauter
        if not self._saut_en_cours:
            on_ground = False
            for element_type, position, taille in elements:
                if element_type == "sol":
                    element_rect = pygame.Rect(position, taille)
                    player_rect = self.get_rect()
                    # Vérifier si le joueur est juste au-dessus du sol
                    if player_rect.colliderect(element_rect) and player_rect.bottom <= element_rect.top + 1:
                        on_ground = True
                        break
            
            if not on_ground:
                self._y += 5  # Appliquer une force de gravité
                self._y = min(self._y, self.window.get_height())  # Ne pas dépasser le bas de l'écran
