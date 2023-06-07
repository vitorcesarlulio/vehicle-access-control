import datetime
import cv2
import os
import PlateRecognition
import Main

# Variaveis globais para controle
# Fator de redução da taxa de quadros (exemplo: reduzindo pela metade)
FATOR_REDUCAO = 10 # 30 frames = 194.553291 segundos 20 frames = 
# Define o tamanho desejado para redução do video
largura = 640
altura = 480

def main():
    """
        Ponto de entrada do arquivo, garante execução principal do programa

        Args:
            empty

        Returns:
            array: array com frames.
    """

    try:
        decreaseFramesArray()
    except Exception as e:
        print(e)

def decreaseFramesArray():
    """
        Faz uma série de tratamentos no vídeo para melhorar a performance:
        1. Reduz quantidade de frames
        2. Redimensiona os frames
        3. Converte para escala de cinza
        4. Delimita área específica (corte no frame)

        Args:
            empty

        Returns:
            empty
    """

    try:
        # Abre o vídeo
        cap = cv2.VideoCapture(Main.video_path, cv2.CAP_FFMPEG)

        # Verifica se o vídeo foi aberto com sucesso
        if not cap.isOpened():
            raise Exception("Não foi possível abrir o vídeo")

        # Lê e processa os frames reduzidos
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break
            
            # Processa o frame atual apenas a cada fator de redução
            if count % FATOR_REDUCAO == 0:
                # Redimensiona o frame
                frame = cv2.resize(frame, (largura, altura))

                # Converte para escala de cinza
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Focar somente em uma parte do video
                frame = frame[altura//2:,:]

                if Main.debug:
                    file_name = datetime.datetime.now().strftime("reduced_video_frames_%H-%M-%S_%f")[:-3] + ".jpg"
                    # Salve o quadro como uma imagem na pasta
                    cv2.imwrite(os.path.join('debug/reduced_video_frames/', f'{file_name}'), frame)

                    # Acompanhar frames
                    cv2.imshow('Reduced Video Frames', frame)

                # Reconhece objetos e extrai texto da placa
                PlateRecognition.main(cv2.imencode('.jpg', frame)[1].tobytes())

                # Espera por uma tecla pressionada para avançar para o próximo frame
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            count += 1

        # Libera os recursos
        cap.release()

        if Main.debug:
            cv2.destroyAllWindows()

    except Exception as e:
        print("Ocorreu um erro:", str(e))