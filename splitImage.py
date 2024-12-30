from PIL import Image
import os

def splitImage(imageRute, directory, splitColumn):
    # Verificar si el archivo existe
    if not os.path.isfile(imageRute):
        print(f"El archivo {imageRute} no existe.")
        return
    
    try:
        # Cargar la imagen
        img = Image.open(imageRute)
        print(f"Imagen cargada con formato: {img.format}")
        img.load()  # Asegurarse de que la imagen se haya cargado completamente
        width, height = img.size
    except Exception as e:
        print(f"Error al cargar la imagen {imageRute}: {e}")
        return

    # Calculas número de divisiones por fila
    squareSize = width // splitColumn
    splitsRow = height // squareSize

    # Crear carpeta destino si no existe
    os.makedirs(directory, exist_ok=True)

    # Dividir y guardar cada tiled
    counter = 0
    for i in range(splitsRow):
        for j in range(splitColumn):
            # Coordenadas del cuadrado
            left = j * squareSize
            top = i * squareSize
            right = left + squareSize
            down = top + squareSize

            # Cortar y guardar el cuadrado
            square = img.crop((left, top, right, down))
            fileName = f"tile_{counter + 1}.png"  # Corregido el nombre del archivo
            square.save(os.path.join(directory, fileName))
            counter += 1  # Asegúrate de que el contador aumente

splitImage("assets/images/tiles/tileset.png", "assets/images/tiles", 10)
