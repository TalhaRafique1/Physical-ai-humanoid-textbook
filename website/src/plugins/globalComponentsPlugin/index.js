module.exports = function (context, options) {
  return {
    name: 'global-components-plugin',
    getClientModules() {
      return [
        require.resolve('./GlobalComponents'),
      ];
    },
  };
};