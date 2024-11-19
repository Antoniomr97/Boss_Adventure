import pygame
import constants
import math

class Weapon():
    def __init__(self, image, bulletImage):
        self.bulletImage = bulletImage
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.shape = self.image.get_rect()
        self.shoot = False
        self.lastShoot = pygame.time.get_ticks()

    def update(self, player):
        shootCD = constants.BULLET_CD
        bullet = None
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

        # detect clicks
        if pygame.mouse.get_pressed()[0] and self.shoot == False and (pygame.time.get_ticks()-self.lastShoot >= shootCD):
            bullet = Bullet(self.bulletImage, self.shape.centerx, self.shape.centery, self.angle)
            self.shoot = True
            self.lastShoot = pygame.time.get_ticks()

        # reset mouse click

        if pygame.mouse.get_pressed()[0] == False:
            self.shoot = False
        return bullet

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

    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y , angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # calculo velocidad

        self.delta_x = math.cos(math.radians(self.angle))* constants.SPEED_BULLET
        self.delta_y = -math.sin(math.radians(self.angle))* constants.SPEED_BULLET

    def update(self):
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

        # comprobar si las balas salieron de pantalla
        if self.rect.right < 0 or self.rect.left > constants.WIDTH_SCREEN or self.rect.top > constants.HEIGHT_SCREEN:
            self.kill()

    def draw(self, interface):
        interface.blit(self.image, (self.rect.centerx,
                                    self.rect.centery - int(self.image.get_height()/2.2)))