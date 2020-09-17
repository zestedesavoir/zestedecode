import Vue from 'vue'
import Vuex from 'vuex'

import StackTrace from 'stacktrace-js'

Vue.use(Vuex)

export default client => new Vuex.Store({
  state: {
    // If the display is column-based or full-screen
    display: 'COLUMNS',

    // In full-screen mode, what panel is active
    active_display: 'CODE',

    // All IDE-relatede data (source code, errors, console…)
    ide: {
      code: `// Spawner un perso en jeu
let perso = new Personnage()

// Changer son nom (modifié directement en réseau, avec des setters)
perso.nom = 'Jean-Michel Jarre'

// Changer sa position, l'avancer d'une case
perso.position.x++

// Taper (un bloc ou une entité)
perso.attaquer()

// Écouter des événements
quand('touche z').faire(événement => perso.position.x++)
quand('clic droit').faire(événement => {
  if (perso.blocCible) {
    perso.blocCible.type = 'PIERRE'
  }
})`,
      console: [],
      errors: []
    },

    // Server-related informations like connection status,
    // ping, other participants, …
    server: {
      status: 'CONNECTED',
      ping: 0
    }
  },

  mutations: {
    set_display (state, display) {
      state.display = display
    },

    set_display_active (state, active_display) {
      state.active_display = active_display
    },

    set_code (state, code) {
      state.ide.code = code
    },

    add_error (state, error) {
      state.ide.errors.push(error)
    },

    clean_errors (state) {
      state.ide.errors = []
    }
  },

  actions: {
    exec_code ({ state, commit }) {
      commit('clean_errors')

      try {
        // We add `document` and `window` to the arguments so the code
        // is *somewhat* sandboxed, because we set them to `undefined`.
        // It's not perfect but it prevents most accidental problems.
        // And if users really want to destroy the web app, it's only
        // on their computer anyway, and a reload fix everything.
        const evald_function = new Function('client', 'document', 'window', state.ide.code)
        evald_function(client, undefined, undefined)
      } catch (e) {
        StackTrace.fromError(e).then(trace => {
          let user_error = {}

          if (e instanceof SyntaxError) {
            // For syntax errors, the stack trace does not contain the eval'd code…
            user_error = {}
          } else {
            const user_errors = trace.filter(call => call.source.indexOf('eval line') !== -1)
            if (!user_errors) return

            // We only keep the main error
            user_error = user_errors[0]

            // As we execute a function, the line numbers are shifted due to the added boilerplate
            if (user_error.lineNumber) {
              user_error.lineNumber -= 2
            }
          }

          commit('add_error', {
            type: e.name,
            message: e.message,
            ...user_error
          })
        })
      }
    }
  },
  modules: {
  }
})
