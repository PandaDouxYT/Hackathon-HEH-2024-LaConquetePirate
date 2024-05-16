import pygame, random

class Objet:
    def __init__(self, nom, type):
        self.__nom = nom
        self.__type = type
        self.__images = {
            "chapeau": "assets/img/chapeau.png",
            "cle": "assets/img/cle.png",
            "coeur": "assets/img/coeur.png",
            "bottes": "assets/img/bottes.png",
            "vin": "assets/img/vin.png",
            "epee": "assets/img/epee.png",
            "hache": "assets/img/hache.png",
            "arc": "assets/img/arc.png"
        }
        self.__loaded_images = {key: pygame.image.load(val) for key, val in self.__images.items()}
    
    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, valeur):
        self.__type = valeur

    def UtiliserObjet(self, joueur):
        if self.__nom == "coeur":
            joueur.modifier_vie(50)
        elif self.__nom == "vin":
            joueur.modifier_vie(25)
        elif self.__nom == "bottes":
            joueur.modifier_saut(1.5)
        elif self.__nom in ["epee", "hache", "arc"]:
            joueur.equipe_arme(self.__nom)

    def lacher_objet(self):
        objets_possibles = ['chapeau', 'cle', 'coeur', 'bottes', 'vin', 'epee', 'hache', 'arc']
        if random.random() < 0.25:  # 25% de chance de lâcher un objet
            objet_lache = random.choice(objets_possibles)
            print(f"L'ennemi a lâché un(e) {objet_lache}.")
            return objet_lache
        else:
            print("L'ennemi n'a rien lâché.")
            return None