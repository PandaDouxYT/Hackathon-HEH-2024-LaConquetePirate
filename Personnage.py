class Personnage:
    def __init__(self):
        self._nom = ""
        self._vie = 100
        self._degats = 0
        self._position = (0 ,0)
        self._inventaire = []

    @property
    def get_position(self):
        return self._position

    
    def deplacer(self, x, y):
        self._position = (x, y)

    def attaquer(self):
        pass

    def calculer_distance(self, opposant_pos):
        x1, y1 = self._position
        x2, y2 = opposant_pos
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return distance
        
