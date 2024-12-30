import constants

class World():
    def __init__(self):
        self.mapTiles = []

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
                tileData = [image, imageRect]
                self.mapTiles.append(tileData)

    def draw(self, surface):
        for tile in self.mapTiles:
            surface.blit(tile[0], tile[1])