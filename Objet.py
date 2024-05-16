import pygame, random

class Objet:

    def __init__(self, nom, type):
        """
        QUI: Duchesne Guillaume & Nathan Isembaert
        QUAND: 16-05-2024
        QUOI: Constructeur de la classe Objet

        Arguments:
        - nom: str
        - type: str

        Retourne:
        - Pas de retour

        """
        self.__nom = nom
        self.__type = type
    
    @property
    def type(self):
        """
        QUI: Duchesne Guillaume & Nathan Isembaert
        QUAND: 16-05-2024
        QUOI: Retourne le type de l'objet

        Arguments:
        - Pas d'arguments

        Retourne:
        - type: str
        
        """
        return self.__type


    def UtiliserObjet(self, joueur):
        """
        QUI: Duchesne Guillaume & Nathan Isembaert
        QUAND: 16-05-2024
        QUOI: Permet d'utiliser un objet

        Arguments:
        - joueur: Joueur

        Retourne:
        - Pas de retour

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
        QUI: Duchesne Guillaume & Nathan Isembaert
        QUAND: 16-05-2024
        QUOI: Permet de lâcher un objet

        Arguments:
        - Pas d'arguments

        Retourne:
        - objetLache: str
        
        """
    
        objets_possibles = ['sword1', 'steak', 'piques']
        objetLache = random.choice(objets_possibles)
        print(f"L'ennemi a lâché un(e) {objetLache}")
        return objetLache
        