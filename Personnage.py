class Personnage:
    def __init__(self, nom, type, degats):
        """
        QUI: Duchesne Guillaume & Anthony Vergeylen & Nathan Isembaert & Ulrich Wilfried Nguepi Kengoum
        QUAND: 14-05-2024
        QUOI: Constructeur de la classe Personnage

        Arguments:
        - nom: str
        - type: str
        - degats: int

        Retourne:
        - Pas de retour
        
        """
        self._nom = nom
        self._vie = 95
        self._degats = degats
        self._type = type
        self._position = (0 ,0)
        self._inventaire = []

    @property
    def get_position(self):
        """
        QUI: Duchesne Guillaume & Anthony Vergeylen & Nathan Isembaert & Ulrich Wilfried Nguepi Kengoum
        QUAND: 14-05-2024
        QUOI: Retourne la position du personnage

        Arguments:
        - Pas d'arguments

        Retourne:
        - position: tuple
        
        """
        return self._position

    def deplacer(self, x, y):
        """
        QUI: Duchesne Guillaume & Anthony Vergeylen & Nathan Isembaert & Ulrich Wilfried Nguepi Kengoum
        QUAND: 14-05-2024
        QUOI: Déplace le personnage

        Arguments:
        - x: int
        - y: int

        Retourne:
        - Pas de retour
        
        """
        self._position = (x, y)

    def Attaquer(self, ennemi):
        """
        QUI: Duchesne Guillaume & Anthony Vergeylen & Nathan Isembaert & Ulrich Wilfried Nguepi Kengoum
        QUAND: 14-05-2024
        QUOI: Attaque l'ennemi

        Arguments:
        - ennemi: Personnage

        Retourne:
        - Pas de retour
        
        """
        distance = self.calculer_distance(ennemi._position)

        if self._type == "longueDistance":
            if distance >= 10:
                if 'arc' in self.__inventaire:
                    ennemi._vie -= 2 * self._degats
                else:
                    ennemi._vie -= self._degats
        elif self._type == "midDistance":
            if 5 <= distance < 10:
                if 'hache' in self.__inventaire:
                    ennemi._vie -= 2 * self._degats
                else:
                    ennemi._vie -= self._degats
        elif self._type == "courteDistance":
            if distance < 5:
                if 'epee' in self.__inventaire:
                    ennemi._vie -= 2 * self._degats
                else:
                    ennemi._vie -= self._degats

    def calculer_distance(self, opposant_pos):
        """
        QUI: Duchesne Guillaume & Anthony Vergeylen & Nathan Isembaert & Ulrich Wilfried Nguepi Kengoum
        QUAND: 14-05-2024
        QUOI: Calcule la distance entre le personnage et un ennemi

        Arguments:
        - opposant_pos: tuple

        Retourne:
        - Pas de retour
        
        """
        x1, y1 = self._position
        x2, y2 = opposant_pos
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return distance
        