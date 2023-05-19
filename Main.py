import PlateRecognition
import AccessControl
import ProcessVideo


def main():
    # Processo video, otimiza
    processVideo = ProcessVideo.main()

    # Reconhece objetos e extrai texto da placa
    # plateRecognition = PlateRecognition.main()

    # Valida a placa
    # accessControl = AccessControl.main()


if __name__ == "__main__":
    main()
