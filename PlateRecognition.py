import os
import random
import cv2
import numpy as np
from google.cloud import vision
from google.cloud.vision_v1 import types
import Useful

debug = 1

def main(frame_bytes):
    # Variavel de ambiente para o arquivo de autenticação do Google Vision
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'google_vision_auth.json'

    # Cria a instância do cliente da API do Google Cloud Vision
    global image_annotator
    image_annotator = vision.ImageAnnotatorClient()

    plate_vertices = findObject(frame_bytes)

    # Verifico se houve algum objeto identificado
    if plate_vertices:
        makeImg(plate_vertices, frame_bytes)    

    #return plate

def findObject(frame_bytes):
    """
        Localiza os objetos de uma imagem utilizando API Google Vision.

        Args:
            frame_bytes: imagem (frame) em formato binario.

        Returns:
            plate_vertices: vertices de onde se localiza a placa.

    """

    image = vision.Image(content=frame_bytes)

    objects = image_annotator.object_localization(
        image=image).localized_object_annotations

    # Armazena os vertices de onde se encontra a placa
    plate_vertices = []

    # Entre os objetos identificados, procura a placa
    for object in objects:
        # Extrair do objecets a confinaça pra salvar no banco
        if object.name == 'License plate' and object.score >= 0.75:
            if debug:
                # Salvando frame que contem um objeto de placa, pra usar de debug
                cv2.imwrite(os.path.join('debug/identified_plate/', f'identified_plate_{random.randint(1, 1000)}.jpg'), cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR))

            # Insere em um array as posições X e Y dos pontos que formam a placa
            # NAO POSSO TER DUAS PLACAS NUMA FOTO (FRAME)
            for vertex in object.bounding_poly.normalized_vertices:
                plate_vertices.append([vertex.x, vertex.y])

    return plate_vertices


def makeImg(plate_vertices, frame_bytes):
    """
        A partir de coordenadas X e Y monta imagem somente da região desejada

        Args:  
            frame_bytes: imagem (frame) em formato binario.
            plate_vertices: vertices de onde se localiza a placa.
        
        Returns:

    """

    imagem = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
    vertices = np.array(plate_vertices)

    # Obtenha a altura e a largura da imagem
    altura, largura, _ = imagem.shape

    # Converta as coordenadas normalizadas para coordenadas de pixel
    vertices_pixel = vertices * np.array([largura, altura])

    # Converta as coordenadas de pixel para inteiro
    vertices_pixel_int = vertices_pixel.astype(np.int32)

    # Obtenha os retângulos delimitadores (x, y, largura, altura) da ROI
    x, y, w, h = cv2.boundingRect(vertices_pixel_int)

    # Recorte a região de interesse da imagem com base nos retângulos delimitadores
    imagem_cortada = cv2.getRectSubPix(imagem, (w, h), (x + w/2, y + h/2))

    if debug:
        # Salvando imagem da placa recortada
        cv2.imwrite(os.path.join('debug/cut_plate/', f'cut_plate_{random.randint(1, 1000)}.jpg'), imagem_cortada)

    #return imagem_bytes


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