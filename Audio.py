# Audio
# + jouerSon(url) : void
# + musicAmbiance(url, isLoop)

import pygame, os

class Audio:
    def __init__(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Initialisation de la classe Audio
        """
        pygame.mixer.init()
        print("Audio initialisé")

    def jouerSon(self, url):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Joue un son
        # url: chemin du fichier son à jouer
        """
        
        path = os.path.join("assets", "son", url)
        son = pygame.mixer.Sound(path)
        son.play()

    def musicAmbiance(self, url, isLoop=False):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Joue une musique d'ambiance
        # url: chemin du fichier musique à jouer
        # isLoop: True si la musique doit être jouée en boucle, False sinon
        """

        path = os.path.join("assets", "son", url)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1 if isLoop else 0)
        pygame.mixer.music.set_volume(0.5)

    def stopMusic(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Arrête la musique en cours
        """
        pygame.mixer.music.stop()