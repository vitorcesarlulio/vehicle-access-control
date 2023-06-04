const db = require('./db');
sequelize = db.sequelize,
  Sequelize = db.Sequelize;

const {
  DataTypes
} = require('sequelize');
const Motoristas = db.sequelize.define('motoristas', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  nome: {
    type: DataTypes.STRING(50)
  },
  sobrenome: {
    type: DataTypes.STRING(50)
  },
  identificacao: {
    type: DataTypes.STRING(50),
    unique: true
  },
  categoria_acesso: {
    type: DataTypes.STRING(50)
  }
}, {
  tableName: 'motoristas',
  timestamps: false
});

module.exports = Motoristas;