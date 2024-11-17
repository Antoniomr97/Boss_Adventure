import pygame
import constants

class Player():
    def __init__(self, x, y, animations):
        self.flip = False
        self.animations = animations
        #Imagen de la animación actual
        self.frame_index = 0 
        #Hora actual en milisegundos
        self.update_time = pygame.time.get_ticks()
        self.image = animations[self.frame_index]
        self.shape = pygame.Rect(0, 0, constants.WIDTH_CHARACTER, constants.HEIGHT_CHARACTER)
        self.shape.center = (x, y)

    def movement(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.shape.x = self.shape.x + delta_x
        self.shape.y = self.shape.y + delta_y

    def update(self):
        cooldown_animation = 200
        self.image = self.animations[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animations):
            self.frame_index = 0

    def draw(self, interface):
        image_flip = pygame.transform.flip(self.image, self.flip, flip_y = False)
        interface.blit(image_flip, self.shape)
        #pygame.draw.rect(interface, constants.COLOR_CHARACTER, self.shape, width=1)
