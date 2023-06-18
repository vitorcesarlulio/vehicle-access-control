const express = require('express');
const path = require('path');
const app = express();

const Veiculo = require("./models/veiculos");
const Acessos = require("./models/acessos");
const Motorista = require("./models/motoristas")

var db = require('./models/db'),
  sequelize = db.sequelize,
  Sequelize = db.Sequelize;

app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');

app.get('/', (req, res) => {
  Acessos.findAll({
    attributes: ['id', 'placa_veiculo', 'id_motorista', 'status_veiculo', 'data_hora_entrada', 'data_hora_saida']
  })
  .then((acessos) => {
    res.render('index', {
      acessos
    });
  })
  .catch((error) => {
    console.log('Erro ao obter os acessos:', error);
    res.status(500).json({ error: 'Erro ao obter os acessos' });
  });
});



app.get('/veiculos', (req, res) => {
  Veiculo.findAll({
      attributes: ['placa', 'marca', 'modelo', 'cor', 'ano', 'status']
    })
    .then((veiculos) => {
      res.json(veiculos);
    })
    .catch((error) => {
      console.log('Erro ao obter os veículos:', error);
      res.status(500).json({
        error: 'Erro ao obter os veículos'
      });
    });
});

app.get('/acessos', (req, res) => {
  Acessos.findAll({
      attributes: ['id', 'placa_veiculo', 'id_motorista', 'status_veiculo', 'data_hora_entrada', 'data_hora_saida']
    })
    .then((Acessos) => {
      res.json(Acessos);
    })
    .catch((error) => {
      console.log('Erro ao obter os veículos:', error);
      res.status(500).json({
        error: 'Erro ao obter os veículos'
      });
    });
});
app.get('/motoristas', (req, res) => {
  Motorista.findAll({
      attributes: ['id', 'nome', 'sobrenome', 'identificacao', 'categoria_acesso']
    })
    .then((motorista) => {
      res.json(motorista);
    })
    .catch((error) => {
      console.log('Erro ao obter os veículos:', error);
      res.status(500).json({
        error: 'Erro ao obter os veículos'
      });
    });
});

app.listen(8080, () => {
  console.log('Servidor rodando na porta 8080');
});