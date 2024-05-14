class Joueur:
    def __init__(self, listePerso, vie, inventaire, xp, niveau):
        self.__listePerso = listePerso
        self.__vie = vie
        self.__inventaire = inventaire
        self.__niveau = niveau
        self.__xp = xp

    @property
    def get_level(self):
        return self.__niveau

    @property
    def get_vie(self):
        return self.__vie

    @property
    def get_inventaire(self):
        return self.__inventaire

    def RecupererObject(self, objet):
        if(objet not in self._inventaire):
            self._inventaire.append(objet)
        else:
            print("Vous possedez déjà cette objet")


    def AjouterNiveau(self):
        if(self.__xp > 100):
            self.__niveau += 1
            self.__xp = 0        

    def Attaquer(self, ennemi):
        distance = self.calculer_distance(ennemi._position)
        if(self._type == "longueDistance"):
            if(distance >= 10):
                ennemi._vie -= self._degats

        elif(self._type == "midDistande"):
            if(5 <= distance < 10):
                ennemi._vie -= self._degats

        elif(self._type == "courteDistande"):
            if(distance < 5):
                ennemi._vie -= self._degats


    def ChangerPersonnage(self):
        pass