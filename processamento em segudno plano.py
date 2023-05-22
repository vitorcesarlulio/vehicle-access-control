import os
import io
import cv2
from google.cloud import vision_v1p3beta1 as vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'google_vision_auth.json'

# Configuração do cliente do Google Vision
client = vision.ImageAnnotatorClient()

# Configuração do vídeo
cap = cv2.VideoCapture('plates_image/video720p.mkv', cv2.CAP_FFMPEG)

# Pré-carregamento dos frames em memória
frames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

# Processamento dos frames em segundo plano
for frame in frames:
    _, buffer = cv2.imencode('.jpg', frame)
    content = buffer.tobytes()
    image = vision.Image(content=content)
    objects = client.object_localization(image=image).localized_object_annotations
    # Processa os resultados da detecção de objetos
    for object_ in objects:
        # extrair do objecets a confinaça pra salvar no banco
        print(objects)
   
    # Salva o frame em disco
    cv2.imwrite('frames/frame{}.jpg'.format(len(frames)), frame)
