class Joueur:
    def __init__(self, niveau, xp):
        self.__niveau = niveau
        self.__xp = xp


        @property
        def niveau(self):
            return self.__niveau

        @niveau.setter
        def niveau(self, valeur):
            self.__niveau = valeur

        @property
        def xp(self):
            return self.__xp

        @xp.setter
        def xp(self, valeur):
            self.__xp = valeur

    def RecupererObject(self):
        pass
    def AjouterNiveau(self):
        pass
    def Attaquer(self):
        pass

    def ChangerPersonnage(self):
        pass



