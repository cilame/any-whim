// 尝试打包 jsdom 成单个文件。

// 安装一个node，我用的是v12版本
// 1 新建一个文件件 在里面的环境下，使用命令 npm init -y
//   将生成文件 package 里面的 scripts 中添加键值对 "build": "webpack"
// 2 在里面安装webpack的库
//   npm install webpack webpack-cli --save
// 3 在里面安装jsdom一些基本需要的库文件
//   npm install crypto-browserify path-browserify url buffer util stream-browserify vm-browserify os-browserify stream-http https-browserify browserify-zlib --save
// 4 新建一个 webpack.config.js 文件写入以下内容
// 5 新建一个 some.js 文件，然后写入下面两行代码
//    const jsdom = require('jsdom');
//    export { jsdom }
// 6 执行 npm run build 等待一会儿即可
// 7 使用的时候在生成的代码后面添加一个 const jsdom = vilame.jsdom;
//   这样 vilame.jsdom 就相当于 require('jsdom') 来使用了。

// 生成的文件最好格式化一下，否则单行内容过长会导致一般的 IDE 编辑卡顿严重难以进行后续编辑
// 这里使用的是python进行的格式化
// # pip install jsbeautifier
// with open('./vilame.js', encoding='utf-8') as f:
//     jscode = f.read()
// import jsbeautifier
// btjscode = jsbeautifier.beautify(jscode)
// with open('./vilame_buti.js', 'w', encoding='utf-8') as f:
//     f.write(btjscode)

const path = require("path");
module.exports = {
  mode:"production",
  entry:"./some.js",
  output:{
    path:path.resolve(__dirname,"dist"),
    filename:"vilame.js",
    library:"vilame",
  },
  target: "node",
  resolve: {
    fallback: {
      "crypto": require.resolve("crypto-browserify"),
      "path": require.resolve("path-browserify"),
      "url": require.resolve("url"),
      "buffer": require.resolve("buffer"),
      "util": require.resolve("util"),
      "stream": require.resolve("stream-browserify"),
      "vm": require.resolve("vm-browserify"),
      "os": require.resolve("os-browserify"),
      "http": require.resolve("stream-http"),
      "https": require.resolve("https-browserify"),
      "zlib": require.resolve("browserify-zlib"),
    },
  },
  externals: {
    "canvas":         "commonjs canvas",
    "utf-8-validate": "commonjs utf-8-validate",
    "bufferutil":     "commonjs bufferutil",
  }
}