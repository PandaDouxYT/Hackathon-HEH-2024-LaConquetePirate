from Personnage import Personnage
from Objet import Objet

class Ennemi(Personnage):
    
    def __init__(self, nom, vie, degats, position, inventaire, schemaAttaque):
        self.__schemaAttaque = schemaAttaque
        super().__init__(nom, vie, degats, position, inventaire)



    def comportement(self, joueur):
        attaquer = False
        distance = self.calculer_distance(joueur._position)

        if(self.__schemaAttaque == 0):
            # L'ennemi attaque si le joueur se raproche trop prés (par exemple distance< 10)
            if(distance < 10):
                attaquer = True
            
        elif(self.__schemaAttaque == 1):
            # L'ennemi attaque en s'éloigna du joueur (pour un ennemi de type long)
            if(distance < 10):
                direction_opposee_x = -1 * (joueur.position[0] - self.position[0])
                direction_opposee_y = -1 * (joueur.position[1] - self.position[1])
                self.deplacer(direction_opposee_x, direction_opposee_y)
                attaquer = False
            else:
                attaquer = True

        elif(self.__schemaAttaque == 2):
            # L'ennemi se raproche du joueur et attaque
            direction_vers_joueur_x = joueur._position[0] - self.position[0]
            direction_vers_joueur_y = joueur._position[1] - self.position[1]
            self.deplacer(direction_vers_joueur_x, direction_vers_joueur_y)
            attaquer = True

        else:
            print("Votre schéma d'attaque n'existe pas")

        return attaquer


    def attaque(self, joueur):
        distance = self.calculer_distance(joueur._position)
        attaquer = self.comportement(self, joueur)

        if(self._type == "longueDistance"):
            if(distance >= 10 and attaquer == True):
                joueur._vie -= self._degats

        elif(self._type == "midDistande"):
            if(5 <= distance < 10 and attaquer == True):
                joueur._vie -= self._degats

        elif(self._type == "courteDistande"):
            if(distance < 5 and attaquer == True):
                joueur._vie -= self._degats

    def verifier_mort(self):
            if self._vie <= 0:
                objet_lache = Objet.lacher_objet()
                if objet_lache:
                    print(f"L'ennemi a lâché un(e) {objet_lache}.")
                    return objet_lache
                else:
                    print("L'ennemi n'a rien lâché.")
                    return None