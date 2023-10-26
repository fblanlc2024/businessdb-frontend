const fs = require('fs');
const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    https: {
      key: fs.readFileSync('D:\\Projects\\Python\\math-quiz\\key.pem'),
      cert: fs.readFileSync('D:\\Projects\\Python\\math-quiz\\cert.pem'),
    }
  }
});