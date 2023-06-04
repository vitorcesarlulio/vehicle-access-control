const Sequelize = require('sequelize')


const sequelize = new Sequelize("controleacesso", "root", "", {
    host: 'localhost',
    dialect: 'mysql',
})

sequelize.authenticate().then(function () {
    console.log('deu bom familia');
}).catch(function () {
    console.log('deu ruim');
});

var db = {};

db.sequelize = sequelize;
db.Sequelize = Sequelize;

module.exports = db;