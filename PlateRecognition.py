from random import randint
import uuid
import re
import os
import cv2
import numpy as np
from google.cloud import vision
import Main
import datetime

score_detection_object = 0.75
extract_plates = []

def main(frame_bytes):
    # Variavel de ambiente para o arquivo de autenticação do Google Vision
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'config/google_vision_auth.json'

    # Cria a instância do cliente da API do Google Cloud Vision
    global image_annotator
    image_annotator = vision.ImageAnnotatorClient()

    try:
        plate_vertices = findObjects(frame_bytes)

        # Verifico se houve algum objeto identificado
        if plate_vertices:
            cut_plate_frame_bytes = cutPlateFrame(plate_vertices, frame_bytes)

            extractTextPlate(cut_plate_frame_bytes)
    except Exception as e:
        print(e)

    #return plate

def findObjects(frame_bytes):
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
        if object.name == 'License plate' and object.score >= score_detection_object:
            if Main.debug:
                file_name = datetime.datetime.now().strftime("identified_plate_%H-%M-%S_%f")[:-3] + ".jpg"
                # Salvando frame que contem um objeto de placa, pra usar de debug
                cv2.imwrite(os.path.join('debug/identified_plate/', f'{file_name}'), cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR))

            # Insere em um array as posições X e Y dos pontos que formam a placa
            for vertex in object.bounding_poly.normalized_vertices:
                plate_vertices.append([vertex.x, vertex.y])

    return plate_vertices


def cutPlateFrame(plate_vertices, frame_bytes):
    """
        A partir de coordenadas X e Y monta imagem somente da região desejada

        Args:  
            frame_bytes: imagem (frame) em formato binario.
            plate_vertices: vertices de onde se localiza a placa.
        
        Returns:
            cut_frame_byes: frame cortado em bytes
    """
    # Realiza decode do frame de bytes para imagem
    frame_image = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)

    vertices = np.array(plate_vertices)

    # Obtenha a altura e a largura da imagem
    altura, largura, _ = frame_image.shape

    # Converta as coordenadas normalizadas para coordenadas de pixel
    vertices_pixel = vertices * np.array([largura, altura])

    # Converta as coordenadas de pixel para inteiro
    vertices_pixel_int = vertices_pixel.astype(np.int32)

    # Obtenha os retângulos delimitadores (x, y, largura, altura) da ROI
    x, y, w, h = cv2.boundingRect(vertices_pixel_int)

    # Recorte a região de interesse da imagem com base nos retângulos delimitadores
    cut_frame = cv2.getRectSubPix(frame_image, (w, h), (x + w/2, y + h/2))

    if Main.debug:
        file_name = datetime.datetime.now().strftime("cut_plate_%H-%M-%S_%f")[:-3] + ".jpg"
        # Salvando imagem da placa recortada
        cv2.imwrite(os.path.join('debug/cut_plate/', f'{file_name}'), cut_frame)

    # Incode da imagem em bytes
    cut_plate_frame_bytes = cv2.imencode('.jpg', cut_frame)[1].tobytes()

    return cut_plate_frame_bytes


def extractTextPlate(cut_plate_frame_bytes):
    image = vision.Image(content=cut_plate_frame_bytes)

    texts = image_annotator.text_detection(
    image=image).text_annotations

    if not texts:
        extract_plates.append("Placa não identificada " + str(uuid.uuid4()))

    # Criando regras regex (não valida nada ainda)
    old_plate_pattern = re.compile(r'^[A-Z]{3}[0-9]{4}$')
    new_plate_pattern = re.compile(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$')

    for text in texts:
        # Removendo caracteres da placa
        clean_plate = text.description.replace(" ", "").replace("-", "")

        # tem que melhorar essa regra
        if len(clean_plate) == 7 and (old_plate_pattern.match(clean_plate) or new_plate_pattern.match(clean_plate)) and (clean_plate not in extract_plates):
            # ignorado os textos de um unico frame que venha só "-" ou "1234"
            extract_plates.append(clean_plate)
        else:
            0==0
            # SE NÃO É UMA PLACA JÁ ERA
            # Só que, se ele identifocu texto da placa porem nao foi classificado como uma placa eu vou perder essa identificação/registro HOJE NAO É NECESSIDADE
            # eu nem teria esse else na teoria, pq seria apenas um texto qualquer na imagem
            # porem, dependendo do frame, da placa, angulo tals, ele pode extrair parte da placa (nao necessariamente nao extrair nenhum caractere)
            #extract_plates.append("Placa não identificada " + str(randint(1, 100))) # essa parte do randomico pode ser falho