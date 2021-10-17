import Vue from 'vue'
import Vuex from 'vuex'

import chat from './chat'
import display from './display'
import ide from './ide'
import loading from './loading'
import server from './server'

Vue.use(Vuex)

export default client => new Vuex.Store({
  modules: {
    chat: chat(client),
    display,
    ide: ide(client),
    loading,
    server: server(client)
  }
})
