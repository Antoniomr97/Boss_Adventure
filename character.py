import pygame
import constants

class Character:
    def __init__(self, x, y, moveAnimations, idleAnimations):
        self.flip = False
        self.walking_animations = moveAnimations
        self.idle_animations = idleAnimations
        self.current_animations = idleAnimations
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.current_animations[self.frame_index]
        self.shape = self.image.get_rect()
        self.shape.center = (x, y)

    def movement(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.shape.x += delta_x
        self.shape.y += delta_y

    def update(self, moving = False):
        # Cambiar entre animaciones
        if moving:
            self.current_animations = self.walking_animations
        else:
            self.current_animations = self.idle_animations

        # Control de la animación
        cooldown_animation = 200
        self.image = self.current_animations[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.current_animations):
            self.frame_index = 0

    def draw(self, interface):
        image_flip = pygame.transform.flip(self.image, self.flip, flip_y=False)
        interface.blit(image_flip, self.shape)
        #pygame.draw.rect(interface, constants.COLOR_CHARACTER, self.shape, width=1)
