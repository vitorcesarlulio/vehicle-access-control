import os
import glob

def delete_directory_files(directory):
    # Obter a lista de todos os arquivos no diretório
    files = glob.glob(os.path.join(directory, '*'))

    # Iterar sobre a lista de arquivos e excluí-los
    for file in files:
        if os.path.isfile(file):
            os.remove(file)