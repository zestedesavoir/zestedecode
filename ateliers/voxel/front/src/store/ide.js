import StackTrace from 'stacktrace-js'

export default client => ({
  namespaced: true,

  state: {
    /**
     * The user' source code, that we'll execute.
     */
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

    /**
     * The console output, if any.
     */
    console: [],

    /**
     * All JavaScript errors caugth during the code's execution.
     */
    errors: []
  },

  mutations: {
    set_code (state, code) {
      state.code = code
    },

    add_error (state, error) {
      state.errors.push(error)
    },

    clean_errors (state) {
      state.errors = []
    }
  },

  actions: {
    async exec_code ({ state, commit }) {
      return new Promise((resolve, reject) => {
        commit('clean_errors')

        try {
          // We add `document`, `window`, `top` and `Function` to the
          // arguments so the code is *somewhat* sandboxed, because we
          // set them to `undefined`.
          //
          // Also, we provide our own versions of `setInterval` and
          // `setTimeout`that refuse string string arguments so this
          // is not a potential leak.
          //
          // It's not perfect but it prevents most accidental problems.
          // And if users really want to destroy the web app, it's only
          // on their computer anyway, and a reload fix everything.

          const __setTimeoutNative__ = window.setTimeout
          const __setIntervalNative__ = window.setInterval

          const neutralizeFunction = function (fn) {
            const func = fn instanceof Function ? function () { return fn.bind({}).apply(null, arguments) } : fn
            return func.bind({})
          }

          const __setTimeoutZest__ = function (fn, timeout) {
            if (typeof fn === 'string') {
              throw new TypeError('setTimeout does not accept source code as string in Zeste de Code')
            }

            return __setTimeoutNative__(neutralizeFunction(fn), timeout, Array.prototype.slice.call(arguments, 2))
          }

          const __setTIntervalZest__ = function (fn, timeout) {
            if (typeof fn === 'string') {
              throw new TypeError('setInterval does not accept source code as string in Zeste de Code')
            }

            return __setIntervalNative__(neutralizeFunction(fn), timeout, Array.prototype.slice.call(arguments, 2))
          }

          const evald_function = new Function(
            'client',
            'document',
            'window',
            'top',
            'Function',
            'setTimeout',
            'setInterval',
            state.code
          ).bind({})

          evald_function(client, undefined, undefined, undefined, undefined, __setTimeoutZest__, __setTIntervalZest__)

          resolve()
        } catch (e) {
          (async () => {
            let user_error = {}

            // For syntax errors, the stack trace does not contain the eval'd code…
            if (!(e instanceof SyntaxError)) {
              const trace = await StackTrace.fromError(e)

              const user_errors = trace.filter(call => call.source.indexOf('eval') !== -1)
              if (!user_errors || user_errors.length === 0) return

              // We only keep the main error
              user_error = user_errors[0]

              // As we execute a function, the line numbers are shifted due to the added boilerplate
              if (user_error.lineNumber) {
                user_error.lineNumber -= 2
              }
            }

            user_error = {
              type: e.name,
              message: e.message,
              ...user_error
            }

            commit('add_error', user_error)
            reject(new Error({ e, user_error }))
          })()
        }
      })
    }
  }
})
