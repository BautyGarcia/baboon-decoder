from PIL import Image
import numpy as np

encoding_table = {
    'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6', 'g': '7', 'h': '8', 'i': '9',
    'j': '10', 'k': '11', 'l': '12', 'm': '13', 'n': '14', 'o': '15', 'p': '16', 'q': '17', 'r': '18',
    's': '19', 't': '20', 'u': '21', 'v': '22', 'w': '23', 'x': '24', 'y': '25', 'z': '26', ' ': '27',
    '.': '28', ',': '29', '?': '30', '!': '31', '¿': '32', '¡': '33', '(': '34', ')': '35', ':': '36',
    ';': '37', '-': '38', '“': '39', "‘": '40', 'á': '41', 'é': '42', 'í': '43', 'ó': '44', 'ú': '45',
    'ü': '46', 'ñ': '47',
}

def setUp(path: str):
    """
    Crea las matrices para poder hacer el filtro de Kuwahara
    
    Argumentos:
        path: Path de la imagen a editar
        
    Return:
        np.array: Matriz de la imagen
    """
    img = Image.open(path)
    matrix = np.array(img)
    return matrix

def applyPadding(matrix: np.array) -> np.array:
    """
    Agrega padding a la matriz de la imagen
    
    Argumentos:
        matrix: Matriz de la imagen
        
    Return:
        np.array: Matriz de la imagen con padding
    """
    return np.pad(matrix, ((2,2), (2,2), (0,0)), "edge")

def get2x2Area(matrix: np.array, pixelCoords: tuple) -> np.array:
    """
    Crea matriz de 2x2 con los valores de la matriz original a partir de un punto
    
    Argumentos:
        matrix: Matriz original
        pixelCoords: Coordenadas del pixel
        
    Return:
        np.array: Matriz de 2x2
    """
    x, y = pixelCoords
    return matrix[x:x+2, y:y+2]

def getMinimumVarianceChannelAverage(area: np.array) -> np.float64:
    """
    Devuelve el promedio de valores del canal con menor varianza de un area de 2x2 sin contar el ultimo pixel
    
    Argumentos:
        area: Area de 2x2
        
    Return:
        np.float64: Promedio de los valores del canal con menor varianza
    """
    
    # Agarro los 3 pixeles que no edito
    variance_pixels = np.array([area[0,0], area[0,1], area[1,0]])
    
    # Obtengo el canal con menor varianza
    min_variance = np.var(variance_pixels, axis=0, ddof=1)

    min_variance_index = np.argmin(min_variance)
    
    # Calculo el promedio de los valores de los pixeles de ese canal y devuelvo
    return np.int64(np.mean(variance_pixels[:, min_variance_index])), min_variance_index

def getValueByKey(key: str) -> str:
    """
    Devuelve el valor de la tabla de codificacion segun la clave
    
    Argumentos:
        key: Clave de la tabla de codificacion
        
    Return:
        str: Valor de la tabla de codificacion
    """
    for k, v in encoding_table.items():
        if v == key:
            return k

def decodeMessage(encoded_message: list) -> str:
    """
    Decodifica el mensaje en base a la tabla de conversion
    
    Argumentos:
        encoded_message: Lista con los numeros del mensaje
        
    Return:
        str: Mensaje decodificado
    """
    message = ""
    acumultaive = ""
    print("Esta es la lista de numeros que me dan para deocdificar: ", encoded_message)
    for number in encoded_message:
        if (number == -1):
            letter = getValueByKey(acumultaive)
            message += letter
            acumultaive = ""
        else:
            acumultaive += str(number - 1)
    
    return message

def decodeImage(image: Image) -> str:
    """
    Decodifica el mensaje de la imagen
    
    Argumentos:
        path: Path de la imagen
        
    Return:
        str: Mensaje decodificado
    """
    image = np.array(image)
    rows, cols, _ = image.shape
    numbers = []
    
    for i in range(0, rows, 2):
        for j in range(0, cols, 2):
            # Obtengo el area de 2x2
            area = get2x2Area(image, (i,j))
            # Obtengo el promedio de los valores del canal con menor varianza
            value_average, min_variance_channel_index = getMinimumVarianceChannelAverage(area)
            # Agarro el valor del pixel con la letra
            message_pixel_value = area[1,1][min_variance_channel_index]
            # Calculo el nuevo valor
            if message_pixel_value - value_average < -1:
                new_pixel_value = message_pixel_value - value_average + 256
            else:
                new_pixel_value = message_pixel_value - value_average
            
            # Si el valor es 0, el mensaje termino
            if new_pixel_value == 0:
                return decodeMessage(numbers)
            
            # Agrego el valor a la lista
            numbers.append(new_pixel_value)