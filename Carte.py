import json

class Carte:
    def __init__(self, map, niveauCarte):
        """
        QUI: Duchesne Guillaume & Ulrich Wilfried Nguepi Kengoum

        QUAND: 15-05-2024
        QUOI: Constructeur de la classe Carte
        
        Arguments:
        - map: liste de string
        - niveauCarte: int

        Retourne:
        - Pas de retour

        """
        self.__map = map
        self.__niveauCarte = niveauCarte

    def charger_carte(self):
        """
        QUI: Duchesne Guillaume & Ulrich Wilfried Nguepi Kengoum
        QUAND: 15-05-2024
        QUOI: Charge la carte actuelle

        Arguments:
        - Pas d'arguments

        Retourne:
        - mapActuelle: dictionnaire

        """

        fichierMap = self.__map[self.__niveauCarte - 1]
        with open(fichierMap, 'r') as fichierChargement:
            mapActuelle = json.load(fichierChargement)
            print("Chargement de la carte...")

        print("map chargée.")
        return mapActuelle