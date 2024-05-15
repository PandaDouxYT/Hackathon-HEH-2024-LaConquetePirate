from Personnage import Personnage
class Joueur:
    def __init__(self, listePerso, inventaire, xp, niveau,vie = 100):
        self.__listePerso = listePerso
        self.__vie = vie
        self.__inventaire = inventaire
        self.__niveau = niveau
        self.__xp = xp
        self.__hauteur_saut = 1.0
        self.__type_arme = None

    @property
    def get_level(self):
        return self.__niveau

    @property
    def vie(self, valeur):
        if valeur > 0:
            self.__vie = valeur
        else:
            self.__vie = 0
            print("Le joueur est mort.")
        print(f"Vie actuelle: {self.__vie}")

    def modifier_vie(self, quantite):
        self.vie += quantite
        if self.__vie < 0:
            self.__vie = 0
            print("Le joueur est mort.")
    

    @property
    def get_inventaire(self):
        return self.__inventaire

    def RecupererObject(self, objet):
        if(objet not in self._inventaire):
            self._inventaire.append(objet)
        else:
            print("Vous possedez déjà cette objet")

    @hauteur_saut.setter
    def hauteur_saut(self, valeur):
        self.__hauteur_saut = valeur

    def modifier_saut(self, multiplicateur):
        self.hauteur_saut *= multiplicateur
        print(f"Hauteur de saut modifiée à: {self.hauteur_saut}")


    def AjouterNiveau(self):
        if(self.__xp > 100):
            self.__niveau += 1
            self.__xp = 0        

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