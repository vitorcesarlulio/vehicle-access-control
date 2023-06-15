# pip install mysql-connector-python

import configparser
import mysql.connector
import logging
import datetime
from datetime import date

# Tempo pra verificar se um veiculo já foi registrado recentemente (minutos) QUANTO MENOS MELHOR
# A chance de ter uma placa duplicada nos ultimos 1 minutos é muito baixa
global OUTPUT_CONTROL_TIME
OUTPUT_CONTROL_TIME = 1
# Tempo para verificar se o veiculo ainda permanece no local (minutos)
global UPDATE_CONTROL_TIME
UPDATE_CONTROL_TIME = 1440 # 24 horas

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


def main(placa):
    #placa = "FVP1260"
    print("Placa: ", placa)

    conn = connect_database()

    if not there_access(placa, conn):
        result, id_record_update = there_access_update(placa, conn)
        if result:
            update_access(id_record_update, conn)
        else:
            vehicle_status_ = vehicle_status(placa, conn)

            insert_access(placa, vehicle_status_, conn)

    disconnect_database(conn)

def configs():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    
    # Lendo as configurações do arquivo
    host = config.get('mysql', 'host')
    user = config.get('mysql', 'user')
    password = config.get('mysql', 'password')
    database = config.get('mysql', 'database')
    
    return host, user, password, database


def connect_database():
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


def disconnect_database(conn):
    try:
        conn.close()
        logging.info("Desconectado do banco de dados.")

    except mysql.connector.Error as error:
        logging.error("Erro ao desconectar-se do banco de dados: %s", error)


def vehicle_status(placa, conn):  # Chamada para estabelecer a conexão
    status = None
    if placa == "3":
        status = VeiculoStatus.NAO_IDENTIFICADO
    else:
        cursor = conn.cursor()

        # daria pra tentar usar aquele metodo 
        consulta_verificar = "SELECT COUNT(placa) FROM veiculos WHERE placa = %s"
        dados_verificar = (placa,)

        cursor.execute(consulta_verificar, dados_verificar)
        resultado_verificar = cursor.fetchone()

        cursor.close()

        if resultado_verificar[0] == 0:
            logging.debug("Veículo não existe no banco de dados!")
            status = VeiculoStatus.NAO_CADASTRADO
        else:
            logging.debug("Veículo já existe no banco de dados!")
            status = VeiculoStatus.CADASTRADO

    return status


def insert_access(placa, status, conn):
    if status == VeiculoStatus.NAO_IDENTIFICADO:
        placa = ""
    cursor = conn.cursor()

    consulta_inserir = """
    INSERT INTO acessos (placa_veiculo, status_veiculo, data_hora_entrada)
    VALUES (%s, %s, NOW())
    """
    dados_inserir = (placa, status)

    cursor.execute(consulta_inserir, dados_inserir)
    conn.commit()
    logging.debug("Veículo inserido com sucesso!")

    cursor.close()


def there_access(placa, conn):
    cursor = conn.cursor()

    consulta_verificar = """
    SELECT COUNT(id) FROM acessos
    WHERE placa_veiculo = %s AND data_hora_entrada BETWEEN NOW() - INTERVAL %s MINUTE AND NOW()
    """
    dados_verificar = (placa, OUTPUT_CONTROL_TIME)

    cursor.execute(consulta_verificar, dados_verificar)
    resultado_verificar = cursor.fetchone()

    if resultado_verificar[0] > 0:
        logging.warning(
            "Entrada já registrada para o veículo no(s) último(s) 1 minuto(s)!")
        cursor.close()
        return True
    else:
        # ou é um novo acesso ou é uma placa que ta saindo
        return False

def there_access_update(placa, conn):
    cursor = conn.cursor()

    consulta_verificar = """
    SELECT id FROM acessos
    WHERE placa_veiculo =  %s 
    AND data_hora_saida = "0000-00-00 00:00:00"
    AND data_hora_entrada BETWEEN NOW() - INTERVAL %s MINUTE AND NOW()
    ORDER BY id DESC
    LIMIT 1
    """
    dados_verificar = (placa, UPDATE_CONTROL_TIME)

    cursor.execute(consulta_verificar, dados_verificar)
    data = cursor.fetchone()

    cursor.close()

    if data:
        # existe um acesso para atualizar
        return True, data[0]
    else:
        # Quer dizer que é um novo acesso, um veiculo novo entrando
        return False, ""


def update_access(id_record_update, conn):
    cursor = conn.cursor()

    query = "UPDATE acessos SET data_hora_saida = NOW() WHERE id = %s"
    dados_verificar = (id_record_update,)

    cursor.execute(query, dados_verificar)
    cursor.fetchone()
    cursor.close()
    conn.commit()


# Execução do programa principal
if __name__ == "__main__":
    main()
