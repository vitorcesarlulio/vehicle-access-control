# pip install mysql-connector-python

import configparser
import mysql.connector
import logging
import datetime
from datetime import date

# Configuração do logger - melhorar a visibilidade dos prints tanto de retorno quanto de erro presentes no código
# Define o nível de logging para INFO
logging.basicConfig(filename='app.log', level=logging.INFO)

# Criação de um manipulador de logging para exibir mensagens no console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.CRITICAL)

# Adiciona o manipulador de console ao logger raiz
logger = logging.getLogger()
logger.addHandler(console_handler)


class VeiculoStatus:
    CADASTRADO = 1
    NAO_CADASTRADO = 2
    NAO_IDENTIFICADO = 3


def main():
    placa = "EAI8695"

    conn = conectar_banco()
    status = verificar_veiculo(placa, conn)
    entrada_existente = verificar_entrada_existente(placa, conn)

    if not entrada_existente:
        inserir_veiculo(placa, status, conn)

    desconectar_banco(conn)

def configs():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    
    # Lendo as configurações do arquivo
    host = config.get('mysql', 'host')
    user = config.get('mysql', 'user')
    password = config.get('mysql', 'password')
    database = config.get('mysql', 'database')
    
    return host, user, password, database


def conectar_banco():
    host, user, password, database = configs()

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if conn.is_connected():
            logging.info("Conexão estabelecida com o banco de dados.")
            return conn

    except mysql.connector.Error as error:
        logging.error("Erro ao conectar-se ao banco de dados: %s", error)


def desconectar_banco(conn):
    try:
        conn.close()
        logging.info("Desconectado do banco de dados.")

    except mysql.connector.Error as error:
        logging.error("Erro ao desconectar-se do banco de dados: %s", error)


def verificar_veiculo(placa, conn):  # Chamada para estabelecer a conexão
    cursor = conn.cursor()

    # daria pra tentar usar aquele metodo 
    consulta_verificar = "SELECT COUNT(placa) FROM veiculos WHERE placa = %s"
    dados_verificar = (placa,)

    cursor.execute(consulta_verificar, dados_verificar)
    resultado_verificar = cursor.fetchone()

    cursor.close()

    if resultado_verificar[0] == 0:
        logging.debug("Veículo não existe no banco de dados!")
        return VeiculoStatus.NAO_CADASTRADO
    else:
        logging.debug("Veículo já existe no banco de dados!")
        return VeiculoStatus.CADASTRADO


def inserir_veiculo(placa, status, conn):
    cursor = conn.cursor()

    consulta_inserir = """
    INSERT INTO acessos (placa_veiculo, status_veiculo, data_hora_entrada)
    VALUES (%s, %s, NOW())
    """
    dados_inserir = (placa, status)
    print("status:", status)

    cursor.execute(consulta_inserir, dados_inserir)
    conn.commit()
    logging.debug("Veículo inserido com sucesso!")

    cursor.close()


def verificar_entrada_existente(placa, conn):
    cursor = conn.cursor()

    consulta_verificar = """
    SELECT COUNT(*) FROM acessos
    WHERE placa_veiculo = %s AND data_hora_entrada BETWEEN NOW() - INTERVAL 5 MINUTE AND NOW()
    """
    dados_verificar = (placa,)

    cursor.execute(consulta_verificar, dados_verificar)
    resultado_verificar = cursor.fetchone()

    if resultado_verificar[0] > 0:
        logging.warning(
            "Entrada já registrada para o veículo nos últimos 5 minutos!")
        cursor.close()
        return True
    else:
        return False


# Execução do programa principal
if __name__ == "__main__":
    main()
