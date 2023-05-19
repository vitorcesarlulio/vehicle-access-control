import cv2
import os

def main():
    """
        Ponto de entrada do arquivo, garante execução principal do programa

        Args:
            empty

        Returns:
            array: array com frames.
    """
    global video_path
    video_path = 'video_plate_recognition.MOV'

    try:
        decreaseFramesArray()
    except Exception as e:
        print(e)
    # finally:
        # Código a ser executado sempre

def decreaseFramesArray():
    """
        Faz uma série de tratamentos no vídeo para melhorar a performance:
        1. Reduz frames
        2. Redimensiona frames
        3. Converte para escala de cinza
        4. Delimita área específica (corte no frame)

        Args:
            empty

        Returns:
            array: array com frames processados.
    """
    try:
        # Abre o vídeo
        cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)

        # Verifica se o vídeo foi aberto com sucesso
        if not cap.isOpened():
            raise Exception("Não foi possível abrir o vídeo")

        # Fator de redução da taxa de quadros (exemplo: reduzindo pela metade)
        fator_reducao = 50

        # Lista para armazenar os frames processados
        frames_processados = []

        # Define o tamanho desejado para redução do video
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
                # Redimensiona o frame
                frame = cv2.resize(frame, (largura, altura))

                # Converte para escala de cinza
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # focar somente na parte que quero do video
                #area = frame[500:, 300:800]
                # focar somente na parte que quero do video
                #area = frame_redimensionado[altura//2:, largura//2:largura]

                # Aplica a equalização de histograma para melhorar o contraste
                # frame = cv2.equalizeHist(frame)

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

    except Exception as e:
        print("Ocorreu um erro:", str(e))

if __name__ == "__main__":
    main()