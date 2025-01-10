import pygame
import constants
import math
import random

class Character:
    def __init__(self, x, y, moveAnimations, idleAnimations, life, type):
        self.score = 0
        self.life = life
        self.alive = True
        self.flip = False
        self.walking_animations = moveAnimations
        self.idle_animations = idleAnimations
        self.current_animations = idleAnimations
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.current_animations[self.frame_index]
        self.shape = self.image.get_rect()
        self.shape.center = (x, y)
        self.type = type


    def movement(self, delta_x, delta_y, obstaclesTiles):
        screenPosition = [0, 0]
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.shape.x += delta_x
        for obstacle in obstaclesTiles:
            if obstacle[1].colliderect(self.shape):
                if delta_x > 0:
                    self.shape.right = obstacle[1].left
                if delta_x < 0:
                    self.shape.left = obstacle[1].right

        self.shape.y += delta_y
        for obstacle in obstaclesTiles:
            # chequeo de colision
            if obstacle[1].colliderect(self.shape):
                if delta_y > 0:
                    self.shape.bottom = obstacle[1].top
                if delta_y < 0:
                    self.shape.top = obstacle[1].bottom

        # Lógica solo aplica al jugador y no enemigos
        if self.type == 1:
            # actualizar la pantalla basado en la posicion del jugador
            # mover la camara izquierda o derecha
            if self.shape.right > (constants.WIDTH_SCREEN - constants.SCREEN_LIMIT):
                screenPosition[0] = (constants.WIDTH_SCREEN - constants.SCREEN_LIMIT) - self.shape.right
                self.shape.right = constants.WIDTH_SCREEN - constants.SCREEN_LIMIT
            if self.shape.left < constants.SCREEN_LIMIT:
                screenPosition[0] = constants.SCREEN_LIMIT - self.shape.left
                self.shape.left = constants.SCREEN_LIMIT
        
            # mover la camara arriba y abajo
            if self.shape.bottom > (constants.HEIGHT_SCREEN - constants.SCREEN_LIMIT):
                screenPosition[1] = (constants.HEIGHT_SCREEN - constants.SCREEN_LIMIT) - self.shape.bottom
                self.shape.bottom = constants.HEIGHT_SCREEN - constants.SCREEN_LIMIT
            if self.shape.top < constants.SCREEN_LIMIT:
                screenPosition[1] = constants.SCREEN_LIMIT - self.shape.top
                self.shape.top = constants.SCREEN_LIMIT
            return screenPosition


    def enemies(self, player, obstaclesTiles, screenPosition, EnemyList):
        clippedLine = ()
        eneDX = 0
        eneDY = 0

        self.shape.x += screenPosition[0]
        self.shape.y += screenPosition[1]

        # Crear linea de vision
        lineOfSight = ((self.shape.centerx, self.shape.centery),
                        (player.shape.centerx, player.shape.centery))
        
        # Comprobar obstaculos
        for obs in obstaclesTiles:
            if obs[1].clipline(lineOfSight):
                clippedLine = obs[1].clipline(lineOfSight)

        distance = math.sqrt(((self.shape.centerx - player.shape.centerx) ** 2) + 
                             ((self.shape.centery - player.shape.centery) ** 2 ))
        
        if not clippedLine and distance < constants.RANGE:
            if self.shape.centerx > player.shape.centerx:
                eneDX = -(constants.SPEED_ENEMIES)
            if self.shape.centerx < player.shape.centerx:
                eneDX = (constants.SPEED_ENEMIES)

            if self.shape.centery > player.shape.centery:
                eneDY = -(constants.SPEED_ENEMIES)
            if self.shape.centery < player.shape.centery:
                eneDY = (constants.SPEED_ENEMIES)

            moving = True

        else:
            moving = False
        

        self.movement(eneDX, eneDY, obstaclesTiles)
        self.update(moving)



    def update(self, moving = False):
        # Comprobar si el personaje está vivo

        if self.life <= 0:
            self.life = 0
            self.alive = False

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
