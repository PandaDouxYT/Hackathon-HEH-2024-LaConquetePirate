

class Personnage:
    def __init__(self):
        self._nom = ""
        self._vie = 100
        self._degats = 0
        self._position = (0 ,0)
        self._inventaire = []

    
    def deplacer(self, x, y):
        self._position = (x, y)

    def attaquer(self, cible):
        cible._vie = cible._vie - self._degats
        
