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
        self.rect = (x, y)

    def update(self):
        cooldownAnimation = 150
        self.image = self.animationList[self.frameIndex]

        if pygame.time.get_ticks() - self.updateTime > cooldownAnimation:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()

        if self.frameIndex >= len(self.animationList):
            self.frameIndex = 0