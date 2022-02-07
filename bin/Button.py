import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self):
        """
        Description: Creates the image for the quit button
        Parameter: none
        Returns: none
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/button.jpg')
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 500
