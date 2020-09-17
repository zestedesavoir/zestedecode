module.exports = {
  pluginOptions: {
    i18n: {
      locale: 'fr',
      fallbackLocale: 'fr',
      localeDir: '../locales',
      enableInSFC: false
    }
  },

  pwa: {
    name: 'Zeste de Code',
    themeColor: '#084663',
    msTileColor: '#084663',
    appleMobileWebAppCapable: 'no',
    appleMobileWebAppStatusBarStyle: 'black-translucent',
    manifestOptions: {
      name: 'Zeste de Code — Atelier Voxel'
    },
    iconPaths: {
      favicon16: 'img/icons/16.png',
      favicon32: 'img/icons/32.png',
      favicon64: 'img/icons/64.png',
      favicon128: 'img/icons/128.png',
      favicon256: 'img/icons/256.png',
      appleTouchIcon: 'img/icons/apple-touch-icon.png',
      maskIcon: 'img/icons/safari-pinned-tab.svg',
      msTileImage: 'img/icons/msapplication-icon-144x144.png'
    }
  }
}
