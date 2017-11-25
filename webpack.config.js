const path = require('path');
//These options tell webpack where to start
//And where to output once its done
//This will find all JS code and dependencies and package into 'bundle.js'
module.exports = {
  entry: './js/main.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js'
  },
  module: {
    rules: [{
      //This is an expression that says 'anything ending .js'
      test: /\.js$/,
      exclude: /node_modules/,
      use: {
        //This tells it to use Babel & React
        loader: 'babel-loader',
        options: {
          presets: ['react']
        }
      }
    }]
  }
}
