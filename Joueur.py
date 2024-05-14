class Joueur:
    def __init__(self, listePerso, inventaire, xp, niveau, vie = 100):
        self.__listePerso = listePerso
        self.__vie = vie
        self.__inventaire = inventaire
        self.__niveau = niveau
        self.__xp = xp
        self.__hauteur_saut = 1.0

        @property
        def get_level(self):
            return self.__niveau

        @property
        def get_vie(self):
            return self.__vie
        
        @setter.vie
        def vie(self, valeur):
            if valeur > 0:
                self.__vie = valeur
            else:
                self.__vie = 0
                print("Le joueur est mort.")
            print(f"Vie actuelle: {self.__vie}")
        
        def modifier_vie(self, quantite):
            if self.vie + quantite >= 0:
                self.vie += quantite  # Utilisation du setter
            else:
                self.vie = 0  # Assurez que la vie ne passe pas en-dessous de 0
                print("Le joueur est mort.")

        @property
        def get_inventaire(self):
            return self.__inventaire

        @property
        def hauteur_saut(self):
            return self.__hauteur_saut

        @hauteur_saut.setter
        def hauteur_saut(self, valeur):
            self.__hauteur_saut = valeur

        def modifier_saut(self, multiplicateur):
            self.hauteur_saut *= multiplicateur
            print(f"Hauteur de saut multipliée par : {self.hauteur_saut}")

        # @property
        # def niveau(self):
        #     return self.__niveau

        # @niveau.setter
        # def niveau(self, valeur):
        #     self.__niveau = valeur

        # @property
        # def xp(self):
        #     return self.__xp

        # @xp.setter
        # def xp(self, valeur):
        #     self.__xp = valeur

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

