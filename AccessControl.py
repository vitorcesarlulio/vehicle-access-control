#pip install mysql-connector-python

import mysql.connector
import logging
import datetime
from datetime import date

# Configuração do logger - melhorar a visibilidade dos prints tanto de retorno quanto de erro presentes no código
logging.basicConfig(filename='app.log', level=logging.INFO)  # Define o nível de logging para INFO

# Criação de um manipulador de logging para exibir mensagens no console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Adiciona o manipulador de console ao logger raiz
logger = logging.getLogger()
logger.addHandler(console_handler)


conn = None  # Declaração da variável de conexão global

class VeiculoStatus:
    CADASTRADO = 1
    NAO_CADASTRADO = 2
    NAO_IDENTIFICADO = 3

def conectar_banco():
    global conn  # Indica que estamos utilizando a variável de conexão global
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1:3306",
            user="root",
            password="root",
            database="ProjetoIntegrador"
        )
        if conn.is_connected():
            logging.info("Conexão estabelecida com o banco de dados.")
            return conn

    except mysql.connector.Error as error:
        logging.error("Erro ao conectar-se ao banco de dados: %s", error)

def desconectar_banco():
    global conn  # Indica que estamos utilizando a variável de conexão global
    try:
        conn.close()
        logging.info("Desconectado do banco de dados.")

    except mysql.connector.Error as error:
        logging.error("Erro ao desconectar-se do banco de dados: %s", error)

def verificar_veiculo(placa):
    conectar_banco()  # Chamada para estabelecer a conexão
    cursor = conn.cursor()

    consulta_verificar = "SELECT COUNT(*) FROM veiculos WHERE placa = %s"
    dados_verificar = (placa,)

    cursor.execute(consulta_verificar, dados_verificar)
    resultado_verificar = cursor.fetchone()

    if resultado_verificar[0] == 0:
        logging.info("Veículo não existe no banco de dados!")
        return VeiculoStatus.NAO_CADASTRADO
    else:
        logging.info("Veículo já existe no banco de dados!")
        return VeiculoStatus.CADASTRADO

    cursor.close()

def inserir_veiculo(placa):
    cursor = conn.cursor()

    consulta_inserir = "INSERT INTO acessos (placa_veiculo) VALUES (%s)"
    dados_inserir = (placa,)

    cursor.execute(consulta_inserir, dados_inserir)
    conn.commit()
    logging.info("Veículo inserido com sucesso!")

    cursor.close()
    

def verificar_entrada_existente(placa):
    hoje = date.today().strftime("%D-%M-%Y")

    cursor = conn.cursor()

    consulta_verificar = "SELECT COUNT(*) FROM acessos WHERE placa_veiculo = %s AND data_entrada = %s"
    dados_verificar = (placa, hoje)

    cursor.execute(consulta_verificar, dados_verificar)
    resultado_verificar = cursor.fetchone()

    if resultado_verificar[0] > 0:
        logging.warning("Entrada já registrada para o veículo no dia de hoje!")
        return True
    else:
        return False

    cursor.close()
    desconectar_banco()  # Chamada para desconectar do banco de dados

def main():
    placa = "EAI8695"

    conectar_banco()
    status = verificar_veiculo(placa)

    if status == VeiculoStatus.CADASTRADO:
        logging.info("Veículo cadastrado.")

        if not verificar_entrada_existente(placa):
            inserir_veiculo(placa)
    elif status == VeiculoStatus.NAO_CADASTRADO:
        logging.warning("Veículo não cadastrado.")

        if not verificar_entrada_existente(placa):
            inserir_veiculo(placa)
    elif status == VeiculoStatus.NAO_IDENTIFICADO:
        logging.warning("Placa não identificada.")
    
    desconectar_banco()

# Execução do programa principal
if __name__ == "__main__":
    main()

# Exemplo de uso do logger
logger.info("Esta é uma mensagem de informação.")
logger.warning("Esta é uma mensagem de aviso.")
logger.error("Esta é uma mensagem de erro.")