import pygame
import constants
from player import Player

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH_SCREEN, constants.HEIGHT_SCREEN))

pygame.display.set_caption("Boss Adventure")

def scaleImages(image, scale):
     w = image.get_width()
     h = image.get_height()
     newImage = pygame.transform.scale(image, size=(w * scale, h * scale))
     return newImage

animations =[]

for i in range(4):
     img = pygame.image.load(f"assets//images//characters//player//walking//Walk{i +1}.png")
     img = scaleImages(img, constants.SCALE_CHARACTER)
     animations.append(img)

player = Player(50, 50, animations)

#Movements Player Vars
move_up = False
move_down = False
move_left = False
move_right = False

#Control de FrameRate
clock = pygame.time.Clock()

run = True

while run:
    
    #A 60 FPS
    clock.tick(constants.FPS)

    screen.fill(constants.COLOR_BG)

    #Calculate player movement
    delta_x = 0
    delta_y = 0

    if move_right == True:
        delta_x = constants.SPEED_CHARACTER

    if move_left == True:
        delta_x = -constants.SPEED_CHARACTER

    if move_up == True:
        delta_y = -constants.SPEED_CHARACTER

    if move_down == True:
        delta_y = constants.SPEED_CHARACTER

    #Move the player

    player.movement(delta_x, delta_y)

    player.update()

    player.draw(screen)

    for event in pygame.event.get():
        #Comprobamos si ha clicado en la X para salir de la ventana
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                move_up = True
            if event.key == pygame.K_s:
                move_down = True

        #Soltar la tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                    move_left = False
            if event.key == pygame.K_d:
                    move_right = False
            if event.key == pygame.K_w:
                    move_up = False
            if event.key == pygame.K_s:
                    move_down = False


    pygame.display.update()
    
pygame.quit()