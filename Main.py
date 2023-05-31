from distutils.log import debug
import PlateRecognition, ProcessVideo, Useful

# Variaveis globais para controle
debug = 1
video_path = 'video_plate_recognition.MOV'

def main():
    if debug:
        Useful.delete_directory_files('debug/reduced_video_frames/')
        Useful.delete_directory_files('debug/cut_plate/')
        Useful.delete_directory_files('debug/identified_plate/')

    # Processo video
    ProcessVideo.main()

    # Reconhece objetos e extrai texto da placa
    # plateRecognition = PlateRecognition.main()

    # Valida a placa
    # accessControl = AccessControl.main()


if __name__ == "__main__":
    main()
