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

pygame.mixer.init()

screen = pygame.display.set_mode((constants.WIDTH_SCREEN, constants.HEIGHT_SCREEN))

pygame.display.set_caption("Boss Adventure")

# variables

screenPosition = [0, 0]


# Fuentes

font = pygame.font.Font("assets/fonts/mago3.ttf", 25)
largeFont = pygame.font.Font("assets/fonts/mago3.ttf", 32)
fontGameOver = pygame.font.Font("assets/fonts/mago3.ttf", 100)
# fontRestart = pygame.font.Font("assets/fonts/mago3.ttf", 40)

gameOverText = fontGameOver.render("Mileurista", True, constants.WHITE)
# textRestartButton = fontRestart.render("Restart", True, constants.BLACK)
winText = fontGameOver.render("The Boss Wins", True, constants.WHITE)


# Importar imagenes

# Cargar la imagen del cursor
cursor_image = pygame.image.load("assets/images/cursor/Puntero.png")  # Asegúrate de que la ruta sea correcta

# Tamaño deseado para el cursor (ajusta a tu preferencia)
cursor_size = (32, 32)  # Ejemplo: redimensionamos a 32x32 píxeles

# Redimensionar la imagen del cursor
cursor_image = pygame.transform.scale(cursor_image, cursor_size)

# Obtener las dimensiones del cursor redimensionado
cursor_width, cursor_height = cursor_image.get_size()

# Definir el hotspot (punto de anclaje del cursor)
cursor_hotspot = (0, 0)  # Puedes ajustar esto según donde deseas que esté el punto de anclaje del cursor

# Crear el objeto del cursor
cursor = pygame.cursors.Cursor(cursor_hotspot, cursor_image)

# Establecer el cursor personalizado
pygame.mouse.set_cursor(cursor)


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

WalkEnemiesAnimations = []

for eni in enemiesTypes:
     tempList = []
     ruteTemp = f"assets//images//characters//enemies//{eni}//walking"
     animationsNum = countElements(ruteTemp)
     for i in range(animationsNum):
          imgEnemy = pygame.image.load(f"{ruteTemp}//{eni}Walking{i+1}.png").convert_alpha()
          imgEnemy = scaleImages(imgEnemy, constants.SCALE_ENEMIES)
          tempList.append(imgEnemy)
     WalkEnemiesAnimations.append(tempList)


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
    for i in range(5):
         if player.life >= ((i+1)*20):
              screen.blit(heartFull, (5+i*50, 5))

         elif player.life > (i * 20) and heartHalfDraw == False :
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

cerdito = Character(1350, 700, WalkEnemiesAnimations[0], IdleEnemiesAnimations[0], 150, 2)
cerdito1 = Character(1250, 700, WalkEnemiesAnimations[0], IdleEnemiesAnimations[0], 150, 2)
cerdito2 = Character(1350, 500, WalkEnemiesAnimations[0], IdleEnemiesAnimations[0], 150, 2)
cerdito3 = Character(1250, 500, WalkEnemiesAnimations[0], IdleEnemiesAnimations[0], 150, 2)
marmala = Character(930, 750, WalkEnemiesAnimations[1], IdleEnemiesAnimations[1], 130, 2)
marmala1 = Character(945, 730, WalkEnemiesAnimations[1], IdleEnemiesAnimations[1], 130, 2)
marmala2 = Character(960, 750, WalkEnemiesAnimations[1], IdleEnemiesAnimations[1], 130, 2)
toxica = Character(100, 500, WalkEnemiesAnimations[2], IdleEnemiesAnimations[2], 50, 2)
toxica1 = Character(200, 480, WalkEnemiesAnimations[2], IdleEnemiesAnimations[2], 50, 2)
toxica2 = Character(150, 500, WalkEnemiesAnimations[2], IdleEnemiesAnimations[2], 50, 2)
toxica3 = Character(170, 470, WalkEnemiesAnimations[2], IdleEnemiesAnimations[2], 50, 2)
toxica4 = Character(120, 500, WalkEnemiesAnimations[2], IdleEnemiesAnimations[2], 50, 2)
toxica5 = Character(250, 500, WalkEnemiesAnimations[2], IdleEnemiesAnimations[2], 50, 2)
cabezon = Character(700, 150, WalkEnemiesAnimations[3], IdleEnemiesAnimations[3], 250, 2)

# Crear lista enemigos
EnemyList = []

EnemyList.append(cerdito)
EnemyList.append(cerdito1)
EnemyList.append(cerdito2)
EnemyList.append(cerdito3)
EnemyList.append(marmala1)
EnemyList.append(marmala2)
EnemyList.append(marmala)
EnemyList.append(toxica)
EnemyList.append(toxica1)
EnemyList.append(toxica2)
EnemyList.append(toxica3)
EnemyList.append(toxica4)
EnemyList.append(toxica5)
EnemyList.append(cabezon)

# Cargar video con moviepy


# Crear Arma clase Weapon

# Creamos el Billete

banknote = Weapon(banknoteImage, bulletsImage)

# Creamos grupo de Sprites

groupDamageText = pygame.sprite.Group()

groupBullets = pygame.sprite.Group()

groupItems = pygame.sprite.Group()

coin = Item(780, 186, 0, coinImages)
coin1 = Item(1440, 70, 0, coinImages)
coin2 = Item(1000, 500, 0, coinImages)

potion = Item(780, 55, 1, [redPotion])
potion1 = Item(1024, 335, 1, [redPotion])

groupItems.add(coin)
groupItems.add(coin1)
groupItems.add(coin2)
groupItems.add(potion)
groupItems.add(potion1)

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

pygame.mixer.music.load("assets\sounds\EvilClub.mp3")
pygame.mixer.music.play(-1)

# banknoteSound = pygame.mixer.Sound("assets\sounds\Banknote.mp3")
# banknoteSound.set_volume(1)






run = True

while run:
    
    #A los FPS marcados
    clock.tick(constants.FPS)

    screen.fill(constants.COLOR_BG)

    drawGrid()


    if player.alive:
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

          screenPosition = player.movement(delta_x, delta_y, world.obstaclesTiles)

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
               # banknoteSound.play()

          for bullet in groupBullets:
               damage, damagePosition = bullet.update(EnemyList, world.obstaclesTiles)
               if damage:
                    damageText = DamageText(damagePosition.centerx, damagePosition.centery, str(damage), font, constants.RED)
                    groupDamageText.add(damageText)

          # Actualizar el daño

          groupDamageText.update(screenPosition)

          # Actualizar items

          groupItems.update(screenPosition, player)

          if cabezon.alive == False:
          # Si "cabezon" no está, reproducir el video
               screen.fill(constants.BLACK)
               textRect = winText.get_rect(center=(constants.WIDTH_SCREEN / 2,
                                                       constants.HEIGHT_SCREEN / 2))
               screen.blit(winText, textRect)
               pygame.display.flip()  # Asegúrate de actualizar la pantalla
               pygame.time.delay(3000)  # Pausa de 5 segundos (5000 milisegundos)
               running = False  # Terminar el juego después de la pausa
    
    # Dibujar Mundo

    world.draw(screen)

    # Dibujar al enemigo
    for eni in EnemyList:
         if eni.life == 0:
              EnemyList.remove(eni)
         if eni.life > 0:
               eni.enemies(player ,world.obstaclesTiles, screenPosition, EnemyList)
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

    # Dibujar items

    groupItems.draw(screen)

    # Dibujar textos

    groupDamageText.draw(screen)
    drawText(f"Tip: {player.score}", font, (255,255,0), 900, 20)

    # Level
    drawText(f"Evil Club", largeFont, constants.WHITE, constants.WIDTH_SCREEN/ 2, 20)

    
    if player.alive == False:
         screen.fill(constants.DARK_RED)
         textRect = gameOverText.get_rect(center=(constants.WIDTH_SCREEN / 2,
                                                  constants.HEIGHT_SCREEN / 2))
         screen.blit(gameOverText, textRect)
         # Restart Buttom
     #     restartButton = pygame.Rect(constants.WIDTH_SCREEN / 2 -100,
     #                                 constants.HEIGHT_SCREEN/ 2 +100, 200, 50)
     #     pygame.draw.rect(screen, constants.YELLOW, restartButton)
     #     screen.blit(textRestartButton, (restartButton.x + 50, restartButton.y + 10))


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