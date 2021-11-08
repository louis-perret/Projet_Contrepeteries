'use strict'

const fs = require('fs');

fs.readFile('dict_en.csv', 'utf8', function (err, data) {
  var dataArray = data.split(/\r?\n/);
  console.log(dataArray);
});
