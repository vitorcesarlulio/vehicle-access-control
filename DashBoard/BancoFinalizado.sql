Conexão do banco: 
server host: 127.0.0.1
port:3306
username:root
database: controleacesso

-- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- 

select * from motoristas m;

CREATE TABLE motoristas (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(50),
  sobrenome VARCHAR(50),
  identificacao VARCHAR(50) UNIQUE,
  categoria_acesso VARCHAR(50)
);

truncate motoristas;

INSERT INTO motoristas (nome, sobrenome, identificacao, categoria_acesso)
VALUES 
    ('Ana', 'Silveira', '1234567890', 'A'),
    ('Carlos', 'Ribeiro', '0987654321', 'B'),
    ('Mariana', 'Ferreira', '2468135790', 'C'),
    ('Rodrigo', 'Oliveira', '1357924680', 'B'),
    ('Isabela', 'Martins', '9876543210', 'A');

-- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- 
   
   
select * from acessos a;


truncate acessos

   INSERT INTO acessos (placa_veiculo, id_motorista, status_veiculo, data_hora_entrada, data_hora_saida)
VALUES 
    ('DEF456', 1, 'Aprovado', '2023-06-03 10:00:00', '2023-06-03 12:00:00'),
    ('GHI789', 2, 'Não aprovado', '2023-06-03 09:00:00', '2023-06-03 11:00:00'),
    ('JKL012', 3, 'Não identificado', '2023-06-03 08:00:00', '2023-06-03 10:30:00'),
    ('MNO345', 4, 'Não aprovado', '2023-06-03 07:00:00', '2023-06-03 09:30:00'),
    ('PQR678', 5, 'Aprovado', '2023-06-03 06:00:00', '2023-06-03 08:30:00');



  CREATE TABLE acessos (
  id INT PRIMARY KEY AUTO_INCREMENT,
  placa_veiculo VARCHAR(10),
  id_motorista INT,
  status_veiculo VARCHAR(50) NOT NULL,
  data_hora_entrada DATETIME,
  data_hora_saida DATETIME,  
  FOREIGN KEY (placa_veiculo) REFERENCES veiculos(placa),
  FOREIGN KEY (id_motorista) REFERENCES motoristas(id),
  FOREIGN KEY (status_veiculo) REFERENCES alertas(tipo_status)
);

-- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- 

truncate veiculos	

INSERT INTO veiculos (placa, marca, modelo, cor, ano, status) VALUES
('DEF456', 'Chevrolet', 'Cruze', 'Preto', 2020, 'Não Aprovado'),
('GHI789', 'Volkswagen', 'Golf', 'Branco', 2019, 'Não Identificado'),
('JKL012', 'Toyota', 'Corolla', 'Vermelho', 2021, 'Não Aprovado'),
('MNO345', 'Honda', 'Civic', 'Azul', 2017, 'Não Aprovado'),
('PQR678', 'Renault', 'Sandero', 'Prata', 2016, 'Aprovado');

-- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- -- // -- // -- 

CREATE TABLE alertas (
  id INT PRIMARY KEY AUTO_INCREMENT,
  tipo_status VARCHAR(50),
  INDEX idx_tipo_status (tipo_status)
);

insert into alertas (id, tipo_status) values
(1, 'Aprovado'),
(2, 'Não aprovado'),
(3, 'Não identificado')


drop table alertas