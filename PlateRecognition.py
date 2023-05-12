import os
import cv2
import numpy as np
from google.cloud import vision



def main():
    # Variavel de ambiente para o arquivo de autenticação do Google Vision
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'google_vision_auth.json'

    # Cria a instância do cliente da API do Google Cloud Vision
    global image_annotator
    image_annotator = vision.ImageAnnotatorClient()

    video = cv2.VideoCapture('plates_image/video720p.mkv', cv2.CAP_FFMPEG)
    # O FFMPEG pode ser mais rápido para alguns formatos de vídeo. 
    # Acelerar a leitura do vídeo com GPU
    #cv2.CAP_DSHOW

    # Ajusta o tamanho do buffer de leitura para 10
    # Isso pode melhorar a velocidade de leitura, especialmente para vídeos de alta resolução.
    video.set(cv2.CAP_PROP_BUFFERSIZE, 10) # acho que só adianta se eles precisarem ser processados varias vezes

    # pré-carrega os primeiros 10 frames na memória
    # o aumento no número de quadros pré-carregados pode aumentar o consumo de memória e afetar a performance do sistema se não houver memória suficiente disponível.
    for i in range(20):  # acho que só adianta se eles precisarem ser processados varias vezes
        video.grab()

    folder_path = 'frames_video/'
    frame_count = 0

    while video.isOpened():
        ret, frame = video.read()

        if not ret:
            break
       
        # Redimensiona os frames para 640x480
        #area = cv2.resize(frame, (640, 480))
        # focar somente na parte que quero do video
        area = frame[500:, 300:800]

        # Converte o quadro para o formato JPEG
        success, encoded_frame = cv2.imencode(".jpg", area)
        content = encoded_frame.tobytes()

        # Salve o quadro como uma imagem na pasta
        frame_path = os.path.join(folder_path, f'frame{frame_count}.jpg')
        cv2.imwrite(frame_path, frame)

        # Incremente o contador de quadros
        frame_count += 1

        #cv2.imshow('FRAME',area)

        #findObject(area)

        # pré-carrega o próximo frame na memória
        video.grab()

        if cv2.waitKey(1) == 27:
            break

    video.release()
    cv2.destroyAllWindows()
    """
    file_name = r'plates_image/placa10.jpg'
    path = f'{file_name}'

    with open(path, 'rb') as image_file:
        content = image_file.read()

    array = findObject(content)

    imagem_bytes = makeImg(array, path)

    plate = extractText(imagem_bytes)"""

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
        print(objects)
        if object_.name == 'License plate':
            # Insere em um array as posições X e Y dos pontos que forma a placa
            for vertex in object_.bounding_poly.normalized_vertices:
                array.append([vertex.x, vertex.y])

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

if __name__ == "__main__":
    main()