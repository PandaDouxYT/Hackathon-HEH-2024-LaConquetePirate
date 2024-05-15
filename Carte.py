import json

class Carte:
    def __init__(self, map, niveauCarte):
        self.__map = map #doit recevoir une liste de json des map
        self.__niveauCarte = niveauCarte

    def charger_carte(self):
        fichierMap = self.__map[self.__niveauCarte - 1]  # Sélectionne la carte suivante
        with open(fichierMap, 'r') as fichierChargement:
            mapActuelle = json.load(fichierChargement)
            print("Chargement de la carte...")

        print("map chargée.")
        return mapActuelle


    def activercheckpoint(self):
        pass

    
