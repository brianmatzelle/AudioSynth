import pygame

class endScreen(pygame.sprite.Sprite):
    def __init__(self):
        """
        Description: Creates the image for the text on the closing screen
        Parameter: none
        Returns: none
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/thankyou.jpg')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 100

