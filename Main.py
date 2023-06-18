import time
from distutils.log import debug
import PlateRecognition, ProcessVideo, Useful

# Variaveis globais para controle
debug = 1
video_path = 'assets/video_plate_recognition.MOV'

def main():

    if debug:
        Useful.delete_directory_files('debug/reduced_video_frames/')
        Useful.delete_directory_files('debug/cut_plate/')
        Useful.delete_directory_files('debug/identified_plate/')

    # Processo video
    ProcessVideo.main()

if __name__ == "__main__":
    inicio = time.time() if debug else 0

    main()

    if debug:
        fim = time.time()
        print("Tempo de execução: {:.6f} segundos".format(fim - inicio))
