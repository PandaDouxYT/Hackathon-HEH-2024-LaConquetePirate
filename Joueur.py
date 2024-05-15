from Personnage import Personnage

class Joueur:
    def __init__(self, personnage, vie=100, inventaire=[], xp=10, niveau=0, piece=0):
        self._vie = vie
        self._inventaire = inventaire
        self._niveau = niveau
        self._xp = xp
        self._piece = piece
        self._hauteur_saut = 1.0
        self._personnage = personnage

    @property
    def get_position(self):
        return self._personnage.get_position
    @property
    def get_level(self):
        return self._niveau

    @property
    def get_vie(self):
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

    def RecupererObject(self, objet):
        if(objet not in self._inventaire):
            self._inventaire.append(objet)
        else:
            print("Vous possedez déjà cette objet")

    @property
    def hauteur_saut(self, valeur):
        self._hauteur_saut = valeur

    def modifier_saut(self, multiplicateur):
        self.hauteur_saut *= multiplicateur
        print(f"Hauteur de saut modifiée à: {self.hauteur_saut}")

    def AjouterNiveau(self):
        if(self._xp > 100):
            self._niveau += 1
            self._xp = 0        

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


    def ChangerPersonnage(self):
        pass