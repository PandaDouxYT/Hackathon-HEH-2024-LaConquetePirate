import Joueur
import Ennemi

class objet:
    def __init__(self, nom, type):
        self.__nom = nom
        self.__type = type
        self.__chap = "chapeau"
        self.__cle = "cle"
        self.__coeur = "coeur"
        self.__bottes = "bottes"
        self.__vin = "vin"
        self.__epee = "epee"
        self.__hache = "hache"
        self.__arc = "arc"

    @property
    def coeur(self):
        return self.__coeur
    
    @coeur.setter
    def coeur(self, valeur):
        self.__coeur = valeur
    
    @property
    def vin(self):
        return self.__vin
    
    @coeur.setter
    def coeur(self, valeur):
        self.__vin = valeur
    
    @property
    def type(self):
        return self.__type
    @property
    def bottes(self):
        return self.__bottes
    
    @bottes.setter
    def bottes(self, valeur):
        self.__bottes = valeur

    @type.setter
    def type(self, valeur):
        self.__type = valeur

    def UtiliserObjet(self, joueur):
        if self.__nom == "coeur":
            joueur.modifier_vie(50)
        elif self.__nom == "vin":
            joueur.modifier_vie(25)
        elif self.__nom == "bottes":
            joueur.modifier_saut(1.5)  # Cette méthode doit être ajoutée à la classe Joueur

    def LacherObjet(self):
        print("Objet lâché.")
