import Vue from 'vue'
import Buefy from 'buefy'
import VueCodemirror from 'vue-codemirror'

import './plugins/fontawesome'

import 'codemirror/lib/codemirror.css'
import 'codemirror/mode/javascript/javascript.js'

import App from './App.vue'
import './registerServiceWorker'
import store from './store'
import Client from './client'

Vue.use(Buefy, {
  defaultIconComponent: 'font-awesome-icon',
  defaultIconPack: 'fas'
})

Vue.use(VueCodemirror, {
  options: {
    mode: 'text/javascript',
    tabSize: 4,
    lineNumbers: true,
    line: true
  }
})

Vue.config.productionTip = false

new Vue({
  store: store(new Client()),
  render: h => h(App)
}).$mount('#app')
