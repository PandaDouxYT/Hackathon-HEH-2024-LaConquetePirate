import pygame, time, os, json
from Personnage import Personnage
from Objet import Objet
from Audio import Audio

class Ennemi(Personnage):
    
    def __init__(self, nom, type, vie, degats, inventaire, schemaAttaque, x=0, y=0):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Constructeur de la classe Ennemi
        
        Arguments:
        - nom: string
        - type: string
        - vie: int
        - degats: int
        - inventaire: list
        - schemaAttaque: int

        Retourne:
        - Pas de retour

        """
        super().__init__(nom, type, degats)
        self.__schemaAttaque = schemaAttaque
        self._x = x
        self._y = y
        self._vie = vie

        self.width = 100
        self.height = 90

        self.window = pygame.display.get_surface()

        self.audio = Audio()
        self.volume_level = self.load_volume()  # Charger le volume initial
        self.audio.set_global_volume(self.volume_level)

        # Load character sprites for animation
        self._idle_image = pygame.image.load("assets/img/character4idle.png")
        self._move_images = [
            pygame.image.load(f"assets/img/character4move{i}.png") for i in range(1, 5)
        ]
        
        # Resize character sprites
        self._current_image = self.resize_image(self._idle_image)
        self._move_images = [self.resize_image(image) for image in self._move_images]
        self._character_height = self._current_image.get_height()

        self._animation_index = 0
        self._animation_time = 0
        self._animation_delay = 90  # Delay in milliseconds

        self._facing_right = True  # Indicates the direction the character is facing

        # Update the position to reflect the initial coordinates
        self.mettre_a_jour_position()

        # Cooldown for attack
        self.dernier_attaque_temps = 0

    def resize_image(self, image):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Redimensionne une image
        
        Arguments:
        - image: pygame.Surface

        Retourne:
        - pygame.Surface

        """
        new_width = 100
        original_width, original_height = image.get_size()
        new_height = int((new_width / original_width) * original_height)
        return pygame.transform.scale(image, (new_width, new_height))

    # Se rapprocher
    def deplacer(self, x, y):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Déplacer l'ennemi vers un point spécifique
        
        Arguments:
        - x: int
        - y: int

        Retourne:
        - Pas de retour

        """
        if abs(x - self._x) < 145:
            self.deplacer_arreter()
        elif x > self._x:
            self.deplacer_droite()
        elif x < self._x:
            self.deplacer_gauche()
        if y - 150 > self._y and self._y < 820:
            self._y += 2
        elif y - 150 < self._y and self._y > 760:
            self._y -= 2
            

    # S'éloigner
    def deplacer_inverse(self, x):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Déplacer l'ennemi en sens inverse
        
        Arguments:
        - x: int

        Retourne:
        - Pas de retour

        """
        if x > self._x:
            self.deplacer_gauche()
        elif x < self._x:
            self.deplacer_droite()

    def deplacer_arreter(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Arrêter le déplacement de l'ennemi
        
        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        self._x += 0
        self.mettre_a_jour_position()

    def deplacer_gauche(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Déplacer l'ennemi vers la gauche
        
        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        self._x -= 3.5
        self.mettre_a_jour_position()
        if self._facing_right:
            self.inverser_direction()
        self.animer_marche()

    def deplacer_droite(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Déplacer l'ennemi vers la droite
        
        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        self._x += 3.5
        self.mettre_a_jour_position()
        if not self._facing_right:
            self.inverser_direction()
        self.animer_marche()

    def get_rect(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Retourne le rectangle de zone de collision de l'ennemi
        
        Arguments:
        - Pas d'arguments

        Retourne:
        - self.rect (Rectangle de zone de collision)

        """
        return self.rect

    def comportement(self, joueur):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Définit le comportement de l'ennemi
        
        Arguments:
        - joueur: Personnage

        Retourne:
        - peutAttaquerJoueur: bool

        """
        peutAttaquerJoueur = False
        positionX, positionY = joueur.get_x_y
        distanceX = self.calculer_distance(positionX)
        self.positionJoueur = (positionX, positionY)

        if self.__schemaAttaque == 0:
            # L'ennemi attaque si le joueur se rapproche trop près (par exemple distance < 10)
            if self._vie < 100:
                self.deplacer(positionX, positionY)
                if distanceX < 10:
                    peutAttaquerJoueur = True
                else:
                    peutAttaquerJoueur = False
                    
        elif self.__schemaAttaque == 1:
            if distanceX < 400:
                self.deplacer_inverse(positionX)
                peutAttaquerJoueur = False
            else:
                self.deplacer_arreter()
                peutAttaquerJoueur = True

        elif self.__schemaAttaque == 2:
            self.deplacer(positionX, positionY)
            peutAttaquerJoueur = True

        else:
            print("Votre schéma d'attaque n'existe pas")

        return peutAttaquerJoueur
    
    @property
    def get_x_y(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Retourne les coordonnées x et y de l'ennemi
        
        Arguments:
        - Pas d'arguments

        Retourne:
        - self._x, self._y (int, int)

        """
        return self._x, self._y

    def attaque(self, joueur, vieJoueur):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Permet à l'ennemi d'attaquer le joueur
        
        Arguments:
        - joueur: Personnage
        - vieJoueur: int

        Retourne:
        - newVieJoueur (int)

        """
        currentVieJoueur = vieJoueur
        newVieJoueur = currentVieJoueur

        current_time = time.time()
        if current_time - self.dernier_attaque_temps >= 4:  # Check for cooldown
            peutAttaquerJoueur = self.comportement(joueur)
            positionX, positionY = joueur.get_x_y
            distanceX = self.calculer_distance(positionX)

            if self._type == "longueDistance":
                if distanceX >= 10 and peutAttaquerJoueur:
                    newVieJoueur -= self._degats
            elif self._type == "midDistance":
                if 5 <= distanceX < 10 and peutAttaquerJoueur:
                    newVieJoueur -= self._degats
            elif self._type == "courteDistance":
                if distanceX < 500 and peutAttaquerJoueur:
                    newVieJoueur -= self._degats

            self.dernier_attaque_temps = current_time

        if newVieJoueur < currentVieJoueur:
            self.audio.jouerSon(os.path.join("coup.mp3"))

        return newVieJoueur

    def afficherPersonnage(self, x, y):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Affiche le personnage à l'écran
        
        Arguments:
        - x: int
        - y: int

        Retourne:
        - Pas de retour

        """
        
        # Display the character without adjusting the y position
        self.window.blit(self._current_image, (x, y))

        self.rect = pygame.Rect(x, y, self.width, self._character_height).inflate(-20, 5)
        self.rectDisplay = pygame.draw.rect(self.window, (255, 0, 0), (self.rect), 1)

    def mettre_a_jour_position(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Mettre à jour la position du personnage
        
        Arguments:

        Retourne:
        - Pas de retour

        """
        self.afficherPersonnage(self._x, self._y)


    def verifier_mort(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Vérifie si l'ennemi est mort
        
        Arguments:
        - Pas d'arguments

        Retourne:
        - objet_lache (Objet)

        """
        if self._vie <= 0:
            objet_lache = Objet.lacher_objet(self)
            self._vie = 1
            self._x = -1000  # Déplacer l'ennemi en dehors de l'écran
            self._y = -1000  # Déplacer l'ennemi en dehors de l'écran
            
            if objet_lache:
                print(f"L'ennemi a lâché un(e) {objet_lache}.")
                return objet_lache
            else:
                print("L'ennemi n'a rien lâché.")
                return None

    def inverser_direction(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Inverser la direction du personnage
        
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
        QUOI: Animer le personnage lorsqu'il marche
        
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

    def calculer_distance(self, opposant_pos):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Calcule la distance entre l'ennemi et un autre personnage
        
        Arguments:
        - opposant_pos: int

        Retourne:
        - Pas de retour

        """
        return abs(opposant_pos - self._x)
    
    def load_volume(self):
        """
        QUI: Duchesne Guillaume & Anthony VERGEYLEN
        QUAND: 16-05-2024
        QUOI: Charge le volume global à partir du fichier settings.json
        
        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                return settings.get("volume", 1.0)
        except FileNotFoundError:
            return 1.0  # Valeur par défaut si le fichier n'existe pas
