const fs = require('fs');
const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    server: {
      type: 'https',
      options: {
        key: fs.readFileSync('D:\\Projects\\Python\\fbla-proj-backend\\key.pem'),
        cert: fs.readFileSync('D:\\Projects\\Python\\fbla-proj-backend\\cert.pem'),
      }
    }
  }
});