// @ts-check

/**
 * @param {import('@docusaurus/types').LoadContext} context
 * @returns {import('@docusaurus/types').Plugin}
 */
module.exports = function createWebpackProxyPlugin(context) {
  return {
    name: 'webpack-proxy-plugin',

    configureWebpack(config, isServer, utils) {
      // Only configure proxy for client-side development
      if (!isServer && process.env.NODE_ENV === 'development') {
        return {
          devServer: {
            proxy: {
              '/api': {
                target: 'http://localhost:8000', // Default backend port
                changeOrigin: true,
                secure: false,
              },
            },
          },
        };
      }
      return {};
    },
  };
};