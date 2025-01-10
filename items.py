import pygame.sprite

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, itemType, animationList):
        pygame.sprite.Sprite.__init__(self)
        self.itemType = itemType # 0 = monedas - 1 = pociones
        self.animationList = animationList
        self.frameIndex = 0
        self.updateTime = pygame.time.get_ticks()
        self.image = self.animationList[self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, screenPosition, player):
        # Reposicionar items basado en el lugar de la camara o pantalla
        self.rect.x += screenPosition[0]
        self.rect.y += screenPosition[1]
        
        # Comprobar colision

        if self.rect.colliderect(player.shape):
            # Coin

            if self.itemType == 0:
                player.score += 1

            # Potions

            elif self.itemType == 1:
                player.life += 50
                if player.life > 100:
                    player.life = 100
            self.kill()

        cooldownAnimation = 170
        self.image = self.animationList[self.frameIndex]

        if pygame.time.get_ticks() - self.updateTime > cooldownAnimation:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()

        if self.frameIndex >= len(self.animationList):
            self.frameIndex = 0