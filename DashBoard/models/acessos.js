const db = require('./db');
const { DataTypes } = require('sequelize');
const Alerta = require('./alertas'); // Importe o modelo Alerta

const Acesso = db.sequelize.define('Acesso', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  placa_veiculo: {
    type: DataTypes.STRING(7),
    allowNull: true
  },
  id_motorista: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  status_veiculo: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: Alerta, // Corrija para Alerta
      key: 'id'
    }
  },
  data_hora_entrada: {
    type: DataTypes.DATE,
    allowNull: false
  },
  data_hora_saida: {
    type: DataTypes.DATE,
    allowNull: false
  }
}, {
  tableName: 'acessos',
  timestamps: false
});

Acesso.belongsTo(Alerta, {
  foreignKey: 'status_veiculo'
});

function atualizarConsulta() {
  Acesso.findAll().then(Acessos => {
    console.log(Acessos);
  }).catch(error => {
    console.error('Erro na consulta:', error);
  });
}
atualizarConsulta();
setInterval(atualizarConsulta, 30000);

module.exports = Acesso;
