import pygame
import constants
import math

class Weapon():
    def __init__(self, image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.shape = self.image.get_rect()

    def update(self, player):
        self.shape.center = player.shape.center
        if player.flip == False:
            self.shape.x += (player.shape.width) / 2.5
            self.rotateWeapon(False)
        if player.flip:
            self.shape.x -= (player.shape.width) / 2.5
            self.rotateWeapon(True)
        self.shape.y += 10

        # Mover el arma con el Mouse
        mousePos = pygame.mouse.get_pos()
        distanceX = mousePos[0] - self.shape.centerx
        distanceY = -(mousePos[1] - self.shape.centery)
        self.angle = math.degrees(math.atan2(distanceY, distanceX))

    def rotateWeapon(self, rotate):
        if rotate:
            imageFlip = pygame.transform.flip(self.original_image,
                                              flip_x=True, flip_y=False)
            self.image = pygame.transform.rotate(imageFlip, self.angle)
        else:
            imageFlip = pygame.transform.flip(self.original_image,
                                              flip_x=False, flip_y=False)
            self.image = pygame.transform.rotate(imageFlip, self.angle)

        # Ajustar el centro tras la rotación
        self.shape = self.image.get_rect(center=self.shape.center)

    def draw(self, interface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        interface.blit(self.image, self.shape)
        # pygame.draw.rect(interface, constants.COLOR_WEAPON, self.shape, width=1)

    
