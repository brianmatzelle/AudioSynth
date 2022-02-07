import pygame
from bin import EndScreen, Button, controller

class Controller:
    def __init__(self, synth):
        """
        Description: Controls the actions of the end screen pygame window
        Parameter: none
        Returns: none
        """
        pygame.init()
        self.width = 960
        self.height = 800
        self.display = pygame.display.set_mode((self.width, self.height))
        self.title = EndScreen.endScreen()
        self.button = Button.Button()
        pygame.display.set_caption("Synthesizer Quit Screen")
        self.STATE = "playing"
        self.display.fill((255, 255, 255))
        self.display.blit(self.title.image, (self.title.rect.x, self.title.rect.y))
        self.display.blit(self.button.image, (self.button.rect.x, self.button.rect.y))
        pygame.display.flip()


    def mainLoop(self):
        """
        Description: Determines whether the screen is running or not
        Parameter: none
        Returns: none
        """
        while True:
            if self.STATE == "playing":
                self.playLoop()
            elif self.STATE == "exit":
                self.quitLoop()

    def playLoop(self):
        """
        Description: Displays the screen and quits the screen if the "quit" button is pushed
        Parameter: none
        Returns: none
        """
        while self.STATE == "playing":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.STATE = "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (self.button.rect.collidepoint(event.pos)):
                        self.STATE = "exit"



    def quitLoop(self):
        """
        Description: quits the screen
        Parameter: none
        Returns: none
        """
        pygame.quit()
        exit()

