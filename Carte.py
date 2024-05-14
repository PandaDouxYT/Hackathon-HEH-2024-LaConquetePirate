
class carte:
    def __init__(self, largeur, hauteur, decor, niveauCarte):
        self.__largeur = largeur
        self.hauteur = hauteur
        self.decor = decor  # Fixed syntax error here

    def affichercarte(self, window):
        import pygame  # Importing pygame within the function to ensure it's loaded when called
        image = pygame.image.load(self.decor)
        window.blit(image, (0, 0))

    def activercheckpoint(self):
        pass
