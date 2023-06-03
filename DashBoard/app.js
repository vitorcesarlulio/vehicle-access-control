const express = require('express');
const path = require('path');
const app = express();

const Veiculo = require("./models/veiculos")

var db = require('./models/db'),
    sequelize = db.sequelize,
    Sequelize = db.Sequelize;

app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');

app.get('/', (req, res) => {
  Veiculo.findAll({ attributes: ['placa', 'marca', 'modelo', 'cor', 'ano', 'status'] })
    .then((veiculos) => {
      res.render('index', { veiculos }); 
    })
    .catch((error) => {
      console.log('Erro ao obter os veículos:', error);
      res.status(500).json({ error: 'Erro ao obter os veículos' });
    }); 
});

app.get('/veiculos', (req, res) => {
  Veiculo.findAll({ attributes: ['placa', 'marca', 'modelo', 'cor', 'ano', 'status'] })
    .then((veiculos) => {
      res.json(veiculos);
    })
    .catch((error) => {
      console.log('Erro ao obter os veículos:', error);
      res.status(500).json({ error: 'Erro ao obter os veículos' });
    });
});

app.listen(8080, () => {
  console.log('Servidor rodando na porta 8080');
});
