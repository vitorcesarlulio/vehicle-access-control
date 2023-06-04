const db = require('./db');
sequelize = db.sequelize,
  Sequelize = db.Sequelize;

const Veiculos = require('./veiculos');
const Motoristas = require('./motoristas');
const Alertas = require('./alertas');

const {
  DataTypes
} = require('sequelize');
const Acessos = db.sequelize.define('acessos', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  placa_veiculo: {
    type: DataTypes.STRING(10)
  },
  id_motorista: {
    type: DataTypes.INTEGER
  },
  status_veiculo: {
    type: DataTypes.STRING(50),
    allowNull: false
  },
  data_hora_entrada: {
    type: DataTypes.DATE
  },
  data_hora_saida: {
    type: DataTypes.DATE
  }
}, {
  tableName: 'acessos',
  timestamps: false
});

Acessos.belongsTo(Veiculos, {
  foreignKey: 'placa_veiculo'
});
Acessos.belongsTo(Motoristas, {
  foreignKey: 'id_motorista'
});
Acessos.belongsTo(Alertas, {
  foreignKey: 'status_veiculo'
});


function atualizarConsulta() {
  Acessos.findAll().then(Acessoss => {
    console.log(Acessoss);
  }).catch(error => {
    console.error('Erro na consulta:', error);
  });
}
atualizarConsulta();
setInterval(atualizarConsulta, 30000);

module.exports = Acessos;