const { DataTypes } = require('sequelize');
const db = require('./db');

const Alerta = db.sequelize.define('Alerta', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  status_veiculo: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: 'status_veiculo',
      key: 'id'
    }
  }
}, {
  tableName: 'alerta',
  timestamps: false
});

module.exports = Alerta;
