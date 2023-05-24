import sys
import cv2
import os
import PlateRecognition
import Useful
import time

debug = 1

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

    if debug:
        Useful.delete_directory_files('debug/reduced_video_frames/')
        Useful.delete_directory_files('debug/cut_plate/')
        Useful.delete_directory_files('debug/identified_plate/')

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
        fator_reducao = 100

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
                frame = frame[altura//2:,:]

                # Aplica a equalização de histograma para melhorar o contraste
                # frame = cv2.equalizeHist(frame)

                if debug:
                    # Salve o quadro como uma imagem na pasta
                    cv2.imwrite(os.path.join('debug/reduced_video_frames/', f'reduced_video_frames_{count}.jpg'), frame)

                    # Acompanhar frames
                    cv2.imshow('Reduced Video Frames', frame)


                # Reconhece objetos e extrai texto da placa
                # passa como parametro o frame ja convertido para imagem
                PlateRecognition.main(cv2.imencode('.jpg', frame)[1].tobytes())

                #time.sleep(1.5)

                # Espera por uma tecla pressionada para avançar para o próximo frame
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            count += 1

        # Libera os recursos
        cap.release()

        # descometnar se usar cv2.imshow
        cv2.destroyAllWindows()

        #return frames_processados

    except Exception as e:
        print("Ocorreu um erro:", str(e))

if __name__ == "__main__":
    main()