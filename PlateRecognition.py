import os
import cv2
import numpy as np
from google.cloud import vision
from google.cloud.vision_v1 import types


def main(content):
    # Variavel de ambiente para o arquivo de autenticação do Google Vision
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'google_vision_auth.json'

    # Cria a instância do cliente da API do Google Cloud Vision
    global image_annotator
    image_annotator = vision.ImageAnnotatorClient()

    findObject(content)

    #return plate

def findObject(content):
    """
    Localiza os objetos de uma imagem utilizando API Google Vision.

    Args:
    path: caminho para o imagem local
    """

    image = vision.Image(content=content)

    objects = image_annotator.object_localization(
        image=image).localized_object_annotations

    # Entre os objetos identificados, procura a placa
    # essa var array teria que ser vertices ou coordenadas e mudar o nome dela em outros lugares tbm
    array = []
    for object_ in objects:
        # extrair do objecets a confinaça pra salvar no banco
        if object_.name == 'License plate':
            print("new", objects)
            # Insere em um array as posições X e Y dos pontos que forma a placa
     #       for vertex in object_.bounding_poly.normalized_vertices:
     #           array.append([vertex.x, vertex.y])

    #return array


def makeImg(array, path):
    """
    A partir de coordenadas X e Y monta imagem somente da região desejada

    Args:
    """
    # tem que melhorar pra ele nao deixar a imagem que ele ta gerando com os lados pretos, ter somente a placa

    # tem que melhorar essa parada de ter que abrir a imagem original
    imagem = cv2.imread(path)
    vertices = np.array(array)

    # Obtenha a altura e a largura da imagem
    altura, largura, _ = imagem.shape

    # Converta as coordenadas normalizadas para coordenadas de pixel
    vertices_pixel = vertices * np.array([largura, altura])

    # Converta as coordenadas de pixel para inteiro
    vertices_pixel_int = vertices_pixel.astype(np.int32)

    # Crie uma máscara para o polígono delimitador
    mascara = np.zeros((altura, largura), dtype=np.uint8)
    cv2.fillPoly(mascara, [vertices_pixel_int], (255, 255, 255))

    # Aplique a máscara na imagem
    imagem_cortada = cv2.bitwise_and(imagem, imagem, mask=mascara)

    # Ao inves de salvar, prepara a imagem para carregar no google vision + performatico
    imagem_bytes = cv2.imencode('.jpg', imagem_cortada)[1].tobytes()

    # Salve a imagem cortada (- performatico)
    # cv2.imwrite("cortado.jpg", imagem_cortada)

    return imagem_bytes


def extractText(imagem_bytes):
    image2 = vision.Image(content=imagem_bytes)

    response2 = image_annotator.text_detection(image=image2)
    texts = response2.text_annotations

    plate = ""
    for text_ in texts:
        # debug
        # print(texts)
        plate_ = text_.description.replace(" ", "").replace("-", "")
        plate__ = plate_.split('\n')
        for txt in plate__:
            if len(txt) == 7:
                plate = txt

        if len(plate_) == 7:
            plate = plate_

    return plate

#if __name__ == "__main__":
#    main()