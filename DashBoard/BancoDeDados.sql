Conexão do banco: 
server host: 127.0.0.1
port:3306
username:root
database: controleacesso
--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

CREATE TABLE veiculos (
  placa VARCHAR(10) PRIMARY KEY,
  marca VARCHAR(50),
  modelo VARCHAR(50),
  cor VARCHAR(50),
  ano INT,
  status VARCHAR(50)
);

CREATE TABLE motoristas (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(50),
  sobrenome VARCHAR(50),
  identificacao VARCHAR(50) UNIQUE,
  categoria_acesso VARCHAR(50)
);

INSERT INTO motoristas (nome, sobrenome, identificacao, categoria_acesso)
VALUES 
    ('Ana', 'Silveira', '1234567890', 'A'),
    ('Carlos', 'Ribeiro', '0987654321', 'B'),
    ('Mariana', 'Ferreira', '2468135790', 'C'),
    ('Rodrigo', 'Oliveira', '1357924680', 'B'),
    ('Isabela', 'Martins', '9876543210', 'A');


CREATE TABLE acessos (
  id INT PRIMARY KEY AUTO_INCREMENT,
  placa_veiculo VARCHAR(10),
  id_motorista INT,
  status_veiculo VARCHAR(50) NOT NULL,
  data_hora_entrada DATETIME,
  data_hora_saida DATETIME,  
  FOREIGN KEY (placa_veiculo) REFERENCES veiculos(placa),
  FOREIGN KEY (id_motorista) REFERENCES motoristas(id),
  FOREIGN KEY (status_veiculo) REFERENCES alertas(id)
);


CREATE TABLE alertas (
  id INT PRIMARY KEY AUTO_INCREMENT,
  tipo_status VARCHAR(50) -- Adicionando índice na coluna tipo_status
);

ALTER TABLE acessos
FOREIGN KEY (status_veiculo)
REFERENCES alertas(id);

drop table alertas;

truncate veiculos

INSERT INTO veiculos (placa, marca, modelo, cor, ano, status) VALUES
('ABC123', 'Ford', 'Fiesta', 'Prata', 2018, 'Aprovado'),
('DEF456', 'Chevrolet', 'Cruze', 'Preto', 2020, 'Não Aprovado'),
('GHI789', 'Volkswagen', 'Golf', 'Branco', 2019, 'Não Identificado'),
('JKL012', 'Toyota', 'Corolla', 'Vermelho', 2021, 'Não Aprovado'),
('MNO345', 'Honda', 'Civic', 'Azul', 2017, 'Não Aprovado'),
('PQR678', 'Renault', 'Sandero', 'Prata', 2016, 'Aprovado'),
('STU901', 'Fiat', 'Palio', 'Vermelho', 2015, 'Não Aprovado'),
('VWX234', 'Nissan', 'Versa', 'Branco', 2022, 'Aprovado'),
('YZA567', 'Hyundai', 'HB20', 'Prata', 2019, 'Aprovado'),
('BCD890', 'Kia', 'Sportage', 'Preto', 2020, 'Aprovado');

select * from acessos a 


INSERT INTO acessos (placa_veiculo, id_motorista, status_veiculo, data_hora_entrada, data_hora_saida) VALUES
('ABC123', 1, 2, '2023-05-24 09:00:00', '2023-05-24 10:30:00'),
('DEF456', 2, 3, '2023-05-24 11:15:00', '2023-05-24 12:45:00'),
('GHI789', 3, 1, '2023-05-24 13:30:00', '2023-05-24 15:00:00')



select * from veiculos v 

Aprovado, Não aprovado e Não identificado?


insert into alertas (id, tipo_status) values
(1, 'Aprovado'),
(2, 'Não aprovado'),
(3, 'Não identificado')


select * from alertas a 



drop table acessos 