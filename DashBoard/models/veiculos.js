const db = require('./db');
  sequelize = db.sequelize,
  Sequelize = db.Sequelize;

  const Veiculo = db.sequelize.define('veiculos', {
    placa: {
        type: db.Sequelize.STRING(10),
        primaryKey: true
    },
    marca: {
        type: db.Sequelize.STRING(50)
    },
    modelo: {
        type: db.Sequelize.STRING(50)
    },
    cor: {
        type: db.Sequelize.STRING(50)
    },
    ano: {
        type: db.Sequelize.INTEGER
    },
    status: {
        type: db.Sequelize.STRING(50)
    }
}, {
    timestamps: false 
});

function atualizarConsulta() {
    Veiculo.findAll().then(veiculos => {
        console.log(veiculos);
    }).catch(error => {
        console.error('Erro na consulta:', error);
    });
}
atualizarConsulta();
setInterval(atualizarConsulta, 60000);

module.exports = Veiculo;
