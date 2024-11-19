import pygame
import constants
from player import Player
from weapon import Weapon

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH_SCREEN, constants.HEIGHT_SCREEN))

pygame.display.set_caption("Boss Adventure")

def scaleImages(image, scale):
    w = image.get_width()
    h = image.get_height()
    newImage = pygame.transform.smoothscale(image, (int(w * scale), int(h * scale))).convert_alpha()  # Cambio por smoothscale
    return newImage

#Importar imagenes

#Animación Idle Player

idle_animations = []

for i in range(4):  # Suponiendo que tienes 4 imágenes para idle
    img = pygame.image.load(f"assets/images/characters/player/idle/Idle{i + 1}.png").convert_alpha()
    img = scaleImages(img, constants.SCALE_CHARACTER)
    idle_animations.append(img)

#Animación Walk Player

walkAnimation =[]

for i in range(4):
    img = pygame.image.load(f"assets/images/characters/player/walking/Walk{i + 1}.png").convert_alpha()
    img = scaleImages(img, constants.SCALE_CHARACTER)
    walkAnimation.append(img)
    

# Arma Billete

banknoteImage = pygame.image.load(f"assets/images/weapons/banknote/image/BankNote.png").convert_alpha()
banknoteImage = scaleImages(banknoteImage, constants.SCALE_WEAPON)

# Bullets

bulletsImage = pygame.image.load(f"assets/images/weapons/banknote/image/BankNote.png").convert_alpha()
bulletsImage = scaleImages(banknoteImage, constants.SCALE_BULLETS)

# Crear un jugador de la clase Player

player = Player(50, 50, walkAnimation, idle_animations)

# Crear Arma clase Weapon

# Creamos el Billete

banknote = Weapon(banknoteImage, bulletsImage)

# Creamos grupo de Sprites

groupBullets = pygame.sprite.Group()

# Movements Player Vars
move_up = False
move_down = False
move_left = False
move_right = False

#Control de FrameRate
clock = pygame.time.Clock()

run = True

while run:
    
    #A los FPS marcados
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

    # Move the player

    player.movement(delta_x, delta_y)

    # Detectar si el jugador se está moviendo
    moving = move_up or move_down or move_left or move_right

    # Actualizar la animación del jugador según su movimiento
    player.update(moving)

    # Actualizar el estado del arma
    bullet = banknote.update(player)

    if bullet:
         groupBullets.add(bullet)

    for bullet in groupBullets:
         bullet.update()

    # Dibujar al jugador
    player.draw(screen)

    # Dibujar el arma
    banknote.draw(screen)

    # Dibujar balas

    for bullet in groupBullets:
         bullet.draw(screen)


    for event in pygame.event.get():
        # Comprobamos si ha clicado en la X para salir de la ventana
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