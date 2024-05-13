
from Personnage import Personnage

class Ennemi(Personnage):

    def __init__(self, nom, vie, degats, position, inventaire, schemaAttaque):
        self.__schemaAttaque = schemaAttaque
        super().__init__(nom, vie, degats, position, inventaire)



    def comportement(self):
        if(self.__schemaAttaque == 0):
            pass
        
        elif(self.__schemaAttaque == 1):
            pass

        elif(self.__schemaAttaque == 2):
            pass

        else:
            print("Votre schéma d'attaque n'existe pas")
        

    def attaque(self, joueur):
        joueur.__vie = joueur.__vie - self.__degats