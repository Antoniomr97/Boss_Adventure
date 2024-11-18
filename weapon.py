import pygame
import constants

class Weapon():
    def __init__(self, image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.shape = self.image.get_rect()

    def update(self, player):
        self.shape.center = player.shape.center
        self.shape.x = self.shape.x + (player.shape.width) / 2.5

    def draw(self, interface):
        interface.blit(self.image, self.shape)
        # pygame.draw.rect(interface, constants.COLOR_WEAPON, self.shape, width=1)