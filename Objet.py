class objet:
    def __init__(self, nom, type):
        self.__nom = nom
        self.__type = type

        @property
        def nom(self):
            return self.__nom
        @nom.setter
        def nom(self, valeur):
            self.__nom = valeur

        @property
        def type(self, valeur):
            return self.__type

        @type.setter
        def type(self, valeur):
            self.__type = valeur

    def UtiliserObjet(self):
        pass
    def LacherObjet(self):
        pass
