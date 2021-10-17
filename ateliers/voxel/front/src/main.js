import Vue from 'vue'
import Buefy from 'buefy'
import VueCodemirror from 'vue-codemirror'

import './plugins/fontawesome'

import 'codemirror/lib/codemirror.css'
import 'codemirror/mode/javascript/javascript.js'

import App from './App.vue'
import './registerServiceWorker'
import store_builder from './store'
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

const client = new Client(
  process.env.VUE_APP_WS_URL.replace('{hostname}', document.location.hostname),
  'zdc-voxel-protocol'
)

const store = store_builder(client)
client.set_store(store)

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
