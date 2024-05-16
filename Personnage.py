class Personnage:
    def __init__(self, nom, type):
        self._nom = nom
        self._vie = 95
        self._degats = 0
        self._type = type
        self._position = (0 ,0)
        self._inventaire = []

    @property
    def get_position(self):
        return self._position

    def deplacer(self, x, y):
        self._position = (x, y)

    def Attaquer(self, ennemi):
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
            x1, y1 = self._position
            x2, y2 = opposant_pos
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            return distance
        