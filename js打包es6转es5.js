// 将需要的文件压缩打包成 es5 语法的，可以打包库文件，这样使用起来就方便很多了。

// 安装
// npm install -g cnpm --registry=https://registry.npm.taobao.org
// npm init -y
// cnpm install webpack-cli webpack -S
// cnpm install babel-cli babel-preset-env -S
// 一行安装
// npm install -g cnpm --registry=https://registry.npm.taobao.org && npm init -y && cnpm install webpack-cli webpack -S && cnpm install babel-cli babel-preset-env -S

// 打包
// npx webpack --entry="./index.js"
// npx babel dist/main.js -d es5 --presets=babel-preset-env
// 一行打包
// npx webpack --entry="./index.js" && npx babel dist/main.js -d es5 --presets=babel-preset-env

// 在 es5/dist 文件夹下找 main.js 就是目标文件了。
// 可以新建一个文件夹命名为 index.js 输入下面两行内容。用上面的方式打包。
// const CryptoJS = require('crypto-js')
// window.CryptoJS = CryptoJS