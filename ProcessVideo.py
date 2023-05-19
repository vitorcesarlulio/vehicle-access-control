import cv2
import os

def main():
    """
    1. Reduz frames
    2. Redimensiona frames
    3. Joga para escala de cinza
    4. Delimita area especifica (corte no frame)

    return um array com frames otimizados
    """
    global video_path
    video_path = 'video_plate_recognition.MOV'

    decreaseFramesArray()

def decreaseFramesArray():
    """
        Retorna um array com frames
    """
    # Abre o vídeo
    cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    # O CAP_FFMPEG pode ser mais rápido para alguns formatos de vídeo. 
    # Acelerar a leitura do vídeo com GPU
    #cv2.CAP_DSHOW ESSE N FUNCIONOU VER COMO USA ELE

    # Verifica se o vídeo foi aberto com sucesso
    if not cap.isOpened():
        print("Não foi possível abrir o vídeo.")

    # Fator de redução da taxa de quadros (exemplo: reduzindo pela metade)
    fator_reducao = 50

    # Lista para armazenar os frames processados
    frames_processados = []

    # reduz tamanho do video
    # define o tamanho desejado
    # PODE SER QUE DE PRA DIMINUIR MAIS AINDA
    largura = 640
    altura = 480

    # Lê e processa os frames reduzidos
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Processa o frame atual apenas a cada fator de redução
        if count % fator_reducao == 0:
            # Faça o processamento desejado no frame aqui
            # Por exemplo, você pode aplicar filtros, realizar detecção de objetos, etc.
            
            # redimensiona o frame, LxA RIMEIRO FAZER ISSO, MAIS INTELIGENTE
            frame = cv2.resize(frame, (largura, altura))

            # converte para escala de cinza
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # focar somente na parte que quero do video
            #area = frame[500:, 300:800]
            # focar somente na parte que quero do video
            #area = frame_redimensionado[altura//2:, largura//2:largura]

            #comprimir o video
           
            # tira informações inuteis do video
            #corrigi problemas de iluminação

            ######### DEBUG - START ###########
            """
            # Converte o quadro para o formato JPEG
            success, encoded_frame = cv2.imencode(".jpg", frame)
            content = encoded_frame.tobytes()

            # Salve o quadro como uma imagem na pasta
            frame_path = os.path.join('frames_video/', f'frame{count}.jpg')
            cv2.imwrite(frame_path, frame)"""
            # acompanhar frames
            cv2.imshow('Frames', frame)
            
            ######### DEBUG - END ###########

            # Armazena o frame processado na lista
            frames_processados.append(frame)

            # Espera por uma tecla pressionada para avançar para o próximo frame
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        count += 1

    # Libera os recursos
    cap.release()

    # descometnar se usar cv2.imshow
    cv2.destroyAllWindows()

    return frames_processados

if __name__ == "__main__":
    main()