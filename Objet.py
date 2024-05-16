import pygame, random

class Objet:
    """
    Classe Objet

    permet de créer un type d'objet spécifique
    """
    def __init__(self, nom, type):
        self.__nom = nom
        self.__type = type
    
    @property
    def type(self):
        return self.__type


    def UtiliserObjet(self, joueur):
        """
        Permet d'utiliser un objet spécifique

        paramètre : l'instance joueur

        retourné : aucun
        """
        if self.__nom == "coeur":
            joueur.modifier_vie(50)
        elif self.__nom == "vin":
            joueur.modifier_vie(25)
        elif self.__nom == "bottes":
            joueur.modifier_saut(1.5)
        elif self.__nom in ["epee", "hache", "arc"]:
            joueur.equipe_arme(self.__nom)

    def lacher_objet(self):
        """
        Permet de choisir un objet a lâcher

        paramètre : aucun

        retourné : l'objet qui a été choisi à lacher.
        """
    
        objets_possibles = ['sword1', 'steak', 'piques']
        objetLache = random.choice(objets_possibles)
        print(f"L'ennemi a lâché un(e) {objetLache}")
        return objetLache
        