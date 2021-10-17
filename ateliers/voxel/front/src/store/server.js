import Vue from 'vue'

const short_date_format = new Intl.DateTimeFormat('fr-FR', {
  hour: 'numeric',
  minute: 'numeric'
})

/**
 * Server-related informations like connection status,
 * ping, other participants, …
 */
export default client => ({
  namespaced: true,

  state: {
    /**
     * Our connection's UUID.
     */
    uuid: null,

    /**
     * Our pseudonym.
     */
    pseudonym: null,

    /**
     * True if the teacher mode is enabled.
     */
    teacher: false,

    /**
     * The connection status. Can be
     * - 'CONNECTING';
     * - 'CONNECTED';
     * - 'DISCONNECTED';
     * - null (before the first connection).
     */
    status: null,

    /**
     * All known users. The key are their UUIDs; the value an object
     * with the following keys:
     * - uuid (the UUID, again);
     * - pseudonym (the displayed name of this user);
     * - teacher (if true, displayed as a teacher with colored name and dedicated section in users list);
     * - online (true if the user is currently online);
     * - self (true if this user is ourself).
     */
    users: {},

    /**
     * The latency with the server.
     */
    ping: 0
  },

  mutations: {
    /**
     * Sets the user's UUID.
     *
     * @param {String} uuid The UUID.
     */
    set_uuid (state, uuid) {
      state.uuid = uuid
    },

    /**
     * Sets the user's pseudonym.
     *
     * @param {String} pseudonym The pseudonym.
     */
    set_pseudonym (state, pseudonym) {
      state.pseudonym = pseudonym
    },

    set_teacher (state, teacher) {
      state.teacher = teacher
    },

    set_status (state, status) {
      state.status = status
    },

    set_ping (state, ping) {
      state.ping = ping
    },

    reset_users (state) {
      state.users = {}
    },

    add_user (state, user) {
      console.log('Adding user', user)

      Vue.set(state.users, user.uuid, user)
    },

    set_user_online_state (state, { uuid, online }) {
      const user = state.users[uuid]
      if (!user) return

      user.online = online

      if (!online) {
        user.last_seen_at = short_date_format.format(new Date())
      }
    },

    set_user_teacher (state, { uuid, teacher }) {
      const user = state.users[uuid]
      if (!user) return

      user.teacher = teacher
    },

    set_user_pseudonym (state, { uuid, pseudonym }) {
      const user = state.users[uuid]
      if (!user) return

      user.pseudonym = pseudonym
    }
  },

  actions: {
    set_pseudonym_and_connect ({ commit, dispatch }, pseudonym) {
      commit('set_pseudonym', pseudonym)
      localStorage.setItem('zestedecode-voxel-pseudonym', pseudonym)

      dispatch('connect')
    },

    async connect ({ commit }) {
      commit('loading/set_loading', {
        title: 'Connexion en cours…',
        subtitle: 'Veuillez patienter quelques instants'
      }, { root: true })

      commit('set_status', 'CONNECTING')

      await client.connect()

      commit('set_status', 'CONNECTED')
      commit('loading/set_loading', null, { root: true })
    },

    change_pseudonym ({ commit }, pseudonym) {
      commit('set_pseudonym', pseudonym)
      localStorage.setItem('zestedecode-voxel-pseudonym', pseudonym)

      client.send_pseudonym_change(pseudonym)
    },

    disconnected_from_socket ({ commit }) {
      commit('set_status', 'DISCONNECTED')
      commit('loading/set_loading', {
        title: 'Connexion perdue',
        subtitle: 'Nous tentons de vous reconnecter…'
      }, { root: true })
    },

    send_teacher_request (_, password) {
      return client.send_teacher_request(password)
    }
  }
})
