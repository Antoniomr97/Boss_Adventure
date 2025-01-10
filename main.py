import pygame
import constants
from character import Character
from weapon import Weapon
from texts import DamageText
from items import Item
from world import World
import os
import csv

# Funciones

# Escalar Imagenes

def scaleImages(image, scale):
    w = image.get_width()
    h = image.get_height()
    newImage = pygame.transform.smoothscale(image, (int(w * scale), int(h * scale))).convert_alpha()  # Cambio por smoothscale
    return newImage

# Función contar elementos

def countElements(directory):
     return len(os.listdir(directory))
     

# Función listar nombres elementos

def nameDirectorys(directory):
     return os.listdir(directory)

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH_SCREEN, constants.HEIGHT_SCREEN))

pygame.display.set_caption("Boss Adventure")

# variables

screenPosition = [0, 0]


# Fuentes

font = pygame.font.Font("assets/fonts/mago3.ttf", 25)


# Importar imagenes

# Vida

heartEmpty = pygame.image.load("assets\images\items\heart\HeartEmpty.png").convert_alpha()
heartEmpty = scaleImages(heartEmpty, constants.SCALE_HEART)

heartHalf = pygame.image.load("assets\images\items\heart\HeartHalf.png").convert_alpha()
heartHalf = scaleImages(heartHalf, constants.SCALE_HEART)

heartFull = pygame.image.load("assets\images\items\heart\HeartFull.png").convert_alpha()
heartFull = scaleImages(heartFull, constants.SCALE_HEART)



# Animación Idle Player

idle_animations = []

for i in range(4):  
    img = pygame.image.load(f"assets/images/characters/player/idle/Idle{i + 1}.png").convert_alpha()
    img = scaleImages(img, constants.SCALE_CHARACTER)
    idle_animations.append(img)

# Animación Walk Player

walkAnimation =[]

for i in range(4):
    img = pygame.image.load(f"assets/images/characters/player/walking/Walk{i + 1}.png").convert_alpha()
    img = scaleImages(img, constants.SCALE_CHARACTER)
    walkAnimation.append(img)
    
# Enemigos

enemiesDirectory = "assets//images//characters//enemies"
enemiesTypes = nameDirectorys(enemiesDirectory)

IdleEnemiesAnimations = []

for eni in enemiesTypes:
     tempList = []
     ruteTemp = f"assets//images//characters//enemies//{eni}//idle"
     animationsNum = countElements(ruteTemp)
     for i in range(animationsNum):
          imgEnemy = pygame.image.load(f"{ruteTemp}//{eni}Idle{i+1}.png").convert_alpha()
          imgEnemy = scaleImages(imgEnemy, constants.SCALE_ENEMIES)
          tempList.append(imgEnemy)
     IdleEnemiesAnimations.append(tempList)


# Arma Billete

banknoteImage = pygame.image.load(f"assets/images/weapons/banknote/image/BankNote.png").convert_alpha()
banknoteImage = scaleImages(banknoteImage, constants.SCALE_WEAPON)

# Bullets

bulletsImage = pygame.image.load(f"assets/images/weapons/banknote/image/BankNote.png").convert_alpha()
bulletsImage = scaleImages(banknoteImage, constants.SCALE_BULLETS)

# Cargar imagenes del mundo

tileList = []
for x in range(constants.TILE_TYPES):
    tileImage = pygame.image.load(f"assets/images/tiles/tile_{x + 1}.png").convert_alpha()

    # Recortar automáticamente para eliminar bordes innecesarios
    tileRect = tileImage.get_bounding_rect()  # Encuentra el área no transparente
    croppedImage = tileImage.subsurface(tileRect)  # Recorta la imagen

    # Escalar la imagen recortada al tamaño del tile
    scaledImage = pygame.transform.scale(croppedImage, (constants.TILE_SIZE, constants.TILE_SIZE))
    tileList.append(scaledImage)

# Cargar imagenes items

redPotion = pygame.image.load("assets\images\items\potion\Potion.png")
redPotion = scaleImages(redPotion, 0.15)

coinImages = []
imagesRoute = "assets\images\items\coin"
numCoinImages = countElements(imagesRoute)

for i in range(numCoinImages):
     img = pygame.image.load(f"assets\images\items\coin\coin{i+1}.png")
     img = scaleImages(img, 0.10)
     coinImages.append(img)

def drawText(text, font, color, x, y):
     img = font.render(text, True, color)
     screen.blit(img, (x,y))

def lifePlayer():
    heartHalfDraw = False
    for i in range(4):
         if player.life >= ((i+1)*25):
              screen.blit(heartFull, (5+i*50, 5))

         elif player.life % 25 >= 0 and heartHalfDraw == False :
              screen.blit(heartHalf, (5+i*50, 5))
              heartHalfDraw = True
         else:
              screen.blit(heartEmpty, (5+i*50, 5))
        
worldData = []



for rows in range(constants.ROWS):
     rows = [34] * constants.COLUMS
     worldData.append(rows)

# Cargar el nivel

with open("assets/levels/level1.csv", newline="") as csvfile:
     reader = csv.reader(csvfile, delimiter=",")
     for x, row in enumerate(reader):
          for y, column in enumerate(row):
               worldData[x][y] = int(column)

world = World()
world.processData(worldData, tileList)

def drawGrid():
     for x in range(30):
          pygame.draw.line(screen, constants.WHITE, (x* constants.TILE_SIZE, 0), (x*constants.TILE_SIZE, constants.HEIGHT_SCREEN))
          pygame.draw.line(screen, constants.WHITE, (0 ,x* constants.TILE_SIZE), (constants.WIDTH_SCREEN ,x*constants.TILE_SIZE ))
     


# Crear un jugador de la clase Player

player = Character(100, 800, walkAnimation, idle_animations, 100, 1)

# Crear Enemigos clase Character

cerdito = Character(400, 300, IdleEnemiesAnimations[0], IdleEnemiesAnimations[0], 100, 2)
marmala = Character(200, 200, IdleEnemiesAnimations[1], IdleEnemiesAnimations[1], 100, 2)
toxica = Character(100, 200, IdleEnemiesAnimations[2], IdleEnemiesAnimations[2], 100, 2)

# Crear lista enemigos
EnemyList = []

EnemyList.append(cerdito)
EnemyList.append(marmala)
EnemyList.append(toxica)


# Crear Arma clase Weapon

# Creamos el Billete

banknote = Weapon(banknoteImage, bulletsImage)

# Creamos grupo de Sprites

groupDamageText = pygame.sprite.Group()

groupBullets = pygame.sprite.Group()

groupItems = pygame.sprite.Group()

coin = Item(350, 25, 0, coinImages)

potion = Item(380, 55, 1, [redPotion])

groupItems.add(coin)
groupItems.add(potion)

# Temporal y borrar

# damageText = DamageText(100, 240, "25", font, constants.RED)

# groupDamageText.add(damageText)

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

    drawGrid()

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

    screenPosition = player.movement(delta_x, delta_y)

    # Detectar si el jugador se está moviendo
    moving = move_up or move_down or move_left or move_right

    # Actualizar mapa

    world.update(screenPosition)

    # Actualizar la animación del jugador según su movimiento
    player.update(moving)

    # Actualizar la animación del enemigo según su movimiento
    for eni in EnemyList:
         eni.update()

    # Actualizar el estado del arma
    bullet = banknote.update(player)

    if bullet:
         groupBullets.add(bullet)

    for bullet in groupBullets:
         damage, damagePosition = bullet.update(EnemyList)
         if damage:
              damageText = DamageText(damagePosition.centerx, damagePosition.centery, str(damage), font, constants.RED)
              groupDamageText.add(damageText)

    # Actualizar el daño

    groupDamageText.update(screenPosition)

    # Actualizar items

    groupItems.update(screenPosition, player)
    
    # Dibujar Mundo

    world.draw(screen)

    # Dibujar al enemigo
    for eni in EnemyList:
         eni.enemies(screenPosition)
         eni.draw(screen)

    # Dibujar el arma
    banknote.draw(screen)

    # Dibujar al jugador
    player.draw(screen)

    # Dibujar balas

    for bullet in groupBullets:
         bullet.draw(screen)

    # Dibujar los corazones

    lifePlayer()

    # Dibujar textos

    groupDamageText.draw(screen)
    drawText(f"Propina: {player.score}", font, (255,255,0), 900, 10)

    # Dibujar items

    groupItems.draw(screen)


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