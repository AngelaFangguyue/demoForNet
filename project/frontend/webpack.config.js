'use strict'
const path = require('path')
const webpack = require('webpack')
const ManifestPlugin = require("webpack-manifest-plugin")
const CleanWebpackPlugin = require('clean-webpack-plugin')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const CleanBuildPlugin = require("webpack-clean-by-manifest-plugin")

function resolve (dir) {
  return path.join(__dirname, '..', dir)
}


module.exports = {

  entry: {
    main: './src/main.js',
    common: [
        "vue",
        "jquery/src/jquery.js",
        "bootstrap/dist/js/bootstrap.js",
        "bootstrap/dist/css/bootstrap.css",
        "element-ui",
        "axios",
    ],
  },

  output: {
    path: path.resolve(__dirname, "../backend/static/dist/"),
    filename: 'js/[name].[hash:7].js',
    publicPath: "/static/dist/"
  },

  resolve: {
    extensions: ['.js', '.vue', '.json'],
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
    }
  },

  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {extractCSS: true}
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        include: [
            path.resolve(__dirname, "src"),
            path.resolve(__dirname, 'node_modules/webpack-dev-server/client'),
            path.resolve(__dirname, 'node_modules/element-ui'),
        ]
      },
      {
        test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: 'img/[name].[hash:7].[ext]'
        }
      },
      {
        test: /\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: 'media/[name].[hash:7].[ext]'
        }
      },
      {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: 'fonts/[name].[hash:7].[ext]'
        }
      },
      {
        test: /\.css$/,
        use: ExtractTextPlugin.extract({
          fallback: "style-loader",
          use: "css-loader"
        })
      },
      {
        test: /\.less$/,
        use: ExtractTextPlugin.extract({
          fallback: "css-loader",
          use: 'less-loader'
        })
      },
    ],
  },

  plugins: [
      new ManifestPlugin(),
      new CleanWebpackPlugin([path.resolve(__dirname, "../backend/static/dist/")], {
        root: path.resolve(__dirname, "../"),
      }),
      new ExtractTextPlugin({
        filename: 'css/[name].[hash:7].css',
        allChunks: true
      }),
      new CleanBuildPlugin()
  ],

  node: {
    // prevent webpack from injecting useless setImmediate polyfill because Vue
    // source contains it (although only uses it if it's native).
    setImmediate: false,
    // prevent webpack from injecting mocks to Node native modules
    // that does not make sense for the client
    dgram: 'empty',
    fs: 'empty',
    net: 'empty',
    tls: 'empty',
    child_process: 'empty'
  }
}

if (process.env.NODE_ENV === "production"){
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production')
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: false,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: false
    })
  ])
}
