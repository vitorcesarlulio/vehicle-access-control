# from PIL import Image # testess
# from imutils.video import VideoStream # ler frames de forma mais eficiente


def leframeseficiente():
    vs = VideoStream(src='meu_video.mp4').start()

    while True:
        frame = vs.read()
        # faça algo com o frame

def trataimg():
    
   # Trata imagem antes do processamento.

    #Args:
    
    file_name_ = r'placa10.jpg'
    image_path = f'images/{file_name_}'

    #with open(image_path, 'rb') as image_file_:
    #	image_content = image_file_.read()

    image_content = Image.open(image_path)

    # Redimensionar a imagem
    width, height = image_content.size
    new_width, new_height = 400, 400
    new_image = image_content.resize((new_width, new_height))

    # Comprimir a imagem
    compressed_image_path = 'compressed.jpg'
    new_image.save(compressed_image_path, optimize=True, quality=50)
    # não da pra mexer tanto na qualidade, vai depender muito da foto, do angulo, se não na extração do texto não sai preciso