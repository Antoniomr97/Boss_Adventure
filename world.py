import constants

obstacles = [ 0 , 1 , 2 , 3 , 4 , 5 , 10 , 15 , 20 , 25 , 30 , 35 , 41 , 42 , 43 , 44 ,  45 , 50 , 55 , 66 , 67 , 36 , 37 ]
class World():
    def __init__(self):
        self.mapTiles = []
        self.obstaclesTiles = []

    def processData(self, data, tileList):
        self.mapTiles = []  # Reiniciar tiles si es necesario
        self.levelLength = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile < 0 or tile >= len(tileList):
                    print(f"Índice fuera de rango: {tile} en posición ({x}, {y})")
                    continue
                image = tileList[tile]
                imageRect = image.get_rect()
                # Coloca las imágenes para llenar todo el tile
                imageRect.topleft = (x * constants.TILE_SIZE, y * constants.TILE_SIZE)
                # Añade las coordenadas iniciales x, y al tileData
                tileData = [image, imageRect, imageRect.centerx, imageRect.centery]
                if tile in obstacles:
                    self.obstaclesTiles.append(tileData)
                self.mapTiles.append(tileData)
                


    def update(self, screenPosition):
        for tile in self.mapTiles:
            if len(tile) < 4:
                print(f"Advertencia: tile incompleto encontrado: {tile}")
                continue  # Saltar tiles con datos incompletos
            # Actualiza las posiciones x, y del tile con el desplazamiento
            tile[2] += screenPosition[0]
            tile[3] += screenPosition[1]
            # Ajusta la posición del rectángulo según las nuevas coordenadas
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.mapTiles:
            if len(tile) < 2:
                print(f"Advertencia: tile inválido encontrado durante el dibujo: {tile}")
                continue
            # Dibuja la superficie en las coordenadas del rectángulo
            surface.blit(tile[0], tile[1])