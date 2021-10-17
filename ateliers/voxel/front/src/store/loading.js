/**
 * App's loading state
 */
export default {
  namespaced: true,

  state: {
    /**
     * Should we display the loader and blur the content?
     */
    active: false,

    /**
     * If the loader is active and this is set to some string,
     * this message will be displayed under the loading animation.
     * Accepts HTML.
     */
    message: null,

    /**
     * If this is set to false, the loading animation will be disabled.
     * Notice: If both this is false and message is null, the loader will
     * fallback to Buefy's default, with a loading animation (but not the
     * same).
     */
    loader: true
  },

  mutations: {
    /**
     * Enables or disables loading.
     *
     * @param {Boolean|String} loading `false` to disable loading; `true` to
     *                                 enable it; a string to enable it with
     *                                 a message.
     */
    set_loading (state, loading) {
      state.active = !!loading

      if (loading && loading !== true) {
        if (typeof loading === 'string') {
          state.message = loading
        } else if (typeof loading === 'object') {
          const title = loading.title || ''
          const subtitle = loading.subtitle || ''
          state.message = `${title}<br /><small>${subtitle}</small>`
        }
      }

      if (!loading) {
        state.message = null
      }
    },

    /**
     * Enables or disables the loading animation from the loading screen.
     *
     * @param {Boolean} display_loader `true` to enable; `false` to disable.
     */
    set_loading_loader (state, display_loader) {
      state.loader = display_loader
    }
  }
}
