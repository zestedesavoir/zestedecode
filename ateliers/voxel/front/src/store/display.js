export default {
  namespaced: true,

  state: {
    code_shown: true
  },

  mutations: {
    set_code_shown (state, shown) {
      state.code_shown = shown
    }
  }
}
