import pygame

class Joueur:
    def __init__(self, personnage, xJoueur, yJoueur, vie=100, inventaire=[], xp=10, niveau=0, piece=0):
        self._vie = vie
        self._inventaire = inventaire
        self._niveau = niveau
        self._xp = xp
        self._piece = piece
        self._hauteur_saut = 1.0
        self._personnage = personnage

        self._saut_en_cours = False
        self._vitesse_saut = -15  # vitesse initiale du saut (négative pour aller vers le haut)
        self._gravite = 1  # gravité affectant le saut
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

        # Set initial position
        self._x = xJoueur
        self._y = yJoueur

        # Display character at initial position
        self.afficherPersonnage(self._x, self._y)

    @property
    def get_position(self):
        return self._personnage.get_position

    @property
    def get_level(self):
        return self._niveau
    
    @property
    def get_x_y(self):
        return self._x, self._y

    @property
    def get_vie(self):
        return self._vie

    def modifier_vie(self, quantite):
        self._vie += quantite
        return self._vie

    @property
    def get_xp(self):
        return self._xp
    
    @property
    def get_piece(self):
        return self._piece

    @property
    def get_inventaire(self):
        return self._inventaire
    
    @property
    def hauteur_saut(self):
        return self._hauteur_saut

    @hauteur_saut.setter
    def hauteur_saut(self, valeur):
        self._hauteur_saut = valeur

    def resize_image(self, image):
        new_width = 100
        original_width, original_height = image.get_size()
        new_height = int((new_width / original_width) * original_height)
        return pygame.transform.scale(image, (new_width, new_height))

    def afficherPersonnage(self, x, y):
        window = pygame.display.get_surface()
        
        # Adjust y to account for the character's height
        adjusted_y = y - self._character_height
        window.blit(self._current_image, (x, adjusted_y))

    def mettre_a_jour_position(self):
        window = pygame.display.get_surface()
        window_height = window.get_height()
        self.afficherPersonnage(self._x, window_height - self._y)

    def sauter(self):
        if not self._saut_en_cours:  # Vérifiez si le joueur n'est pas déjà en train de sauter
            self._saut_en_cours = True
            self._vitesse_actuelle_saut = self._vitesse_saut * self._hauteur_saut


    def RecupererObject(self, objet):
        if(objet not in self._inventaire):
            self._inventaire.append(objet)
        else:
            print("Vous possedez déjà cette objet")

    def modifier_saut(self, multiplicateur):
        self._hauteur_saut *= multiplicateur
        print(f"Hauteur de saut modifiée à: {self._hauteur_saut}")

    def AjouterNiveau(self):
        if(self._xp > 100):
            self._niveau += 1
            self._xp = 0        


    def ChangerPersonnage(self, personnage_id):
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
        self._x -= 5  # Déplace le joueur de 5 pixels à gauche
        self.mettre_a_jour_position()
        if self._facing_right:
            self.inverser_direction()
        self.animer_marche()

    def deplacer_droite(self):
        self._x += 5  # Déplace le joueur de 5 pixels à droite
        self.mettre_a_jour_position()
        if not self._facing_right:
            self.inverser_direction()
        self.animer_marche()

    def inverser_direction(self):
        self._facing_right = not self._facing_right
        self._current_image = pygame.transform.flip(self._current_image, True, False)
        self._move_images = [pygame.transform.flip(image, True, False) for image in self._move_images]

    def animer_marche(self):
        current_time = pygame.time.get_ticks()
        if current_time - self._animation_time > self._animation_delay:
            self._animation_index = (self._animation_index + 1) % len(self._move_images)
            self._current_image = self._move_images[self._animation_index]
            self._animation_time = current_time
