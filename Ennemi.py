from Personnage import Personnage


class Ennemi(Personnage):

    def __init__(self, nom, vie, degats, position, inventaire, schemaAttaque):
        self.__schemaAttaque = schemaAttaque
        super().__init__(nom, vie, degats, position, inventaire)



    def comportement(self):
        if(self.__schemaAttaque == 0):
            # schéma d'attaque de pièges, l'ennemi pose des pièges et lorsque celui-ci tombe dedans l'ennemi attaque
            pass
        
        elif(self.__schemaAttaque == 1):
            # schéma d'attaque de projectiles, l'ennemi utilise ses capacités a lancer des sorts, projectiles sur le joueur
            pass

        elif(self.__schemaAttaque == 2):
            pass

        else:
            print("Votre schéma d'attaque n'existe pas")
        

    def attaque(self, joueur):
        joueur.__vie = joueur.__vie - self.__degats