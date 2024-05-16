import pygame, os, json


class Audio:
    def __init__(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Initialisation de la classe Audio

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        pygame.mixer.init()
        print("Audio initialisé")
        self.sounds = []  # Liste pour stocker les sons

        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.global_volume = settings["volume"]
        except FileNotFoundError:
            self.global_volume = 1.0

    def jouerSon(self, url):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Joue un son

        Arguments:
        - url: chemin du fichier son à jouer

        Retourne:
        - Pas de retour
        
        """
        path = os.path.join("assets", "son", url)
        son = pygame.mixer.Sound(path)
        son.set_volume(
            self.global_volume
        )  # Définir le volume du son selon le volume global
        self.sounds.append(son)  # Ajouter le son à la liste
        son.play()

    def musicAmbiance(self, url, isLoop=False):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 13-05-2024
        QUOI: Joue une musique d'ambiance

        Arguments:
        - url: chemin du fichier musique à jouer
        - isLoop: True si la musique doit être jouée en boucle, False sinon

        Retourne:
        - Pas de retour

        """
        path = os.path.join("assets", "son", url)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1 if isLoop else 0)
        pygame.mixer.music.set_volume(
            self.global_volume
        )  # Définir le volume de la musique selon le volume global

    def stopMusic(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 14-05-2024
        QUOI: Arrête la musique en cours

        Arguments:
        - Pas d'arguments

        Retourne:
        - Pas de retour

        """
        pygame.mixer.music.stop()

    def set_global_volume(self, volume):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 15-05-2024
        QUOI: Définit le volume global

        Arguments:
        - volume: float (entre 0.0 et 1.0)

        Retourne:
        - Pas de retour

        """
        self.global_volume = volume
        pygame.mixer.music.set_volume(volume)
        for sound in self.sounds:
            sound.set_volume(volume)

    def get_global_volume(self):
        """
        QUI: Anthony VERGEYLEN
        QUAND: 15-05-2024
        QUOI: Obtient le volume global
        
        Arguments:
        - Pas d'arguments

        Retourne:
        - volume global (float)

        """
        return self.global_volume
