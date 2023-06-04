const db = require('./db');
sequelize = db.sequelize,
  Sequelize = db.Sequelize;

const {
  DataTypes
} = require('sequelize');
const Alertas = db.sequelize.define('alertas', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  tipo_status: {
    type: DataTypes.STRING(50),
    allowNull: false,
    unique: true,
    index: {
      name: 'idx_tipo_status',
      type: 'INDEX'
    }
  }
}, {
  tableName: 'alertas',
  timestamps: false
});

module.exports = Alertas;