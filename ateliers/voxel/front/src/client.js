import MarkdownIt from 'markdown-it'
import { SnackbarProgrammatic as Snackbar } from 'buefy'

const md = new MarkdownIt({
  linkify: true,
  breaks: true,
  typographer: false,
  html: false
})

const debug = (process.env.NODE_ENV || 'development') !== 'production'

export default class Client {
  /**
   * Constructor.
   *
   * @param {string} ws_url The websocket URL to connect to.
   * @param {string} protocol The protocol to expose to the websocket.
   */
  constructor (ws_url, protocol) {
    this.ws_url = ws_url
    this.protocol = protocol || 'zds-voxel-protocol'

    this.client = null
    this.client_uuid = null
    this.secret = null

    this.ping_task = null
  }

  /**
   * Sets the VueX store to use to store data.
   *
   * @param {VueX.Store} store The VueX store.
   */
  set_store (store) {
    this.store = store
  }

  /**
   * Sets the UUID and secret sent by the server and sent back in every message.
   */
  set_uuid_and_secret (uuid, secret) {
    this.client_uuid = uuid
    this.secret = secret
    this.store.commit('server/set_uuid', uuid)

    this.persist_credentials()
  }

  /**
   * Persists the UUID and secret into the session storage, to be able to
   * reconnect in the tab without loosing the link with out “account”.
   */
  persist_credentials () {
    // We must use sessionStorage, else the same UUID/secret may be
    // used between two tabs, and the server does not like this at
    // all (the first client kinda no longer exist for the server).
    // Also, this ensure we cannot track the player with its UUID,
    // as the browser will delete this as soon as the tab or the
    // browser is closed.
    sessionStorage.setItem(
      'zdc-credentials',
      JSON.stringify({
        uuid: this.client_uuid,
        secret: this.secret
      })
    )
  }

  /**
   * Removes the persisted credentials from the session storage.
   */
  delete_persisted_credentials () {
    sessionStorage.removeItem('zdc-credentials')
  }

  /**
   * Loads persisted credentials from the session storage.
   */
  load_persisted_credentials () {
    let credentials = sessionStorage.getItem('zdc-credentials') || ''
    try {
      credentials = JSON.parse(credentials)
    } catch {
      return
    }

    if (!credentials.uuid || !credentials.secret) {
      return
    }

    this.set_uuid_and_secret(credentials.uuid, credentials.secret)
  }

  /**
   * Connects to the websocket using the pseudonym in the store.
   *
   * @return {Promise} A Promise that will be resolved when the connection is
   * successful.
   */
  connect () {
    this.load_persisted_credentials()
    this.kicked = false

    if (this.ping_task) {
      clearInterval(this.ping_task)
    }

    return new Promise((resolve, reject) => {
      this.client = new WebSocket(this.ws_url, this.protocol)

      this.client.onerror = error => {
        console.error('WS initial connection error.')
        reject(error)
      }

      this.client.onopen = () => {
        this.handshake().then(() => resolve())
      }

      this.client.onclose = () => {
        this.client.close()

        this.store.dispatch('server/disconnected_from_socket')
        setTimeout(() => this.store.dispatch('server/connect'), 2000)
      }

      this.client.onmessage = message => {
        if (typeof message.data !== 'string') {
          console.warn(
            'Ignored non-string message received through websocket.',
            message
          )
          return
        }

        if (message.data.startsWith('pong!')) {
          this.message_in_pong(message.data.slice(5))
          return
        }

        let data = null

        try {
          data = JSON.parse(message.data)
        } catch (error) {
          return
        }

        if (!data.action) {
          return
        }

        this.handle_message(data.action, data)
      }
    })
  }

  handshake () {
    // Setup the ping task
    this.ping_task = setInterval(() => {
      this.send_raw_message(`ping!${performance.now()}`)
    }, (debug ? 240000 : 6000) + Math.random() * 2000)

    // Reset the known users. If we lost connection and reconnect, the server will
    // send all users again.
    this.store.commit('server/reset_users')

    // Send handshake message to initialize everything with the server.
    return this.send_message('handshake', {
      pseudonym: this.store.state.server.pseudonym
    })
  }

  /**
   * Reconnects to the game if the connection is lost.
   *
   * @return {Promise} A Promise resolved when the connection is re-established.
   */
  async reconnect () {
    await this.connect()
  }

  /**
   * Sends a message through the websocket.
   *
   * Credentials will automatically be injected.
   *
   * @param {string} action The message's action.
   * @param {object} message The payload can be any JSON-serializable object.
   *
   * @return {Promise} A Promise resolved when the message is successfully sent.
   * If the connection is broken, the promise is rejected with "disconnected".
   */
  send_message (action, message) {
    message = message || {}
    message.action = action
    message.uuid = this.client_uuid
    message.secret = this.secret

    return this.send_raw_message(JSON.stringify(message))
  }

  /**
   * Sends a message as-is to the websocket server.
   *
   * @param {String} message The message to send.
   */
  send_raw_message (message) {
    return new Promise((resolve, reject) => {
      if (this.client.readyState === this.client.OPEN) {
        this.client.send(message)
        resolve()
      } else {
        reject(new Error('disconnected'))
      }
    })
  }

  /**
   * Internal method to handle an incoming message and call the appropriate
   * method.
   *
   * @param {string} action The incoming message's action.
   * @param {object} message The received payload.
   */
  handle_message (action, message) {
    const method_name = 'message_in_' + action.replace(/-/g, '_').trim().toLowerCase()

    if (typeof this[method_name] === 'function') {
      this[method_name](message)
    }
  }

  message_in_set_uuid ({ uuid, secret }) {
    this.set_uuid_and_secret(uuid, secret)
  }

  message_in_pong (time) {
    const ping = performance.now() - time
    this.store.commit('server/set_ping', ping)
  }

  message_in_user_join ({ uuid, pseudonym, online, teacher, realtime }) {
    const user = this.store.state.server.users[uuid]

    if (user) {
      this.store.commit('server/set_user_online_state', {
        uuid,
        online: online
      })
    } else {
      this.store.commit('server/add_user', {
        uuid,
        pseudonym,
        self: uuid === this.uuid,
        online: online,
        teacher: teacher
      })
    }

    if (realtime !== false) {
      this.store.commit('chat/add_chat', {
        channel: 'global',
        type: 'system',
        icon: 'join',
        message: `${pseudonym} a rejoint le salon de discussion`
      })
    }
  }

  message_in_user_left ({ uuid }) {
    const user = this.store.state.server.users[uuid]
    if (!user) return

    this.store.commit('server/set_user_online_state', {
      uuid,
      online: false
    })

    this.store.commit('chat/add_chat', {
      channel: 'global',
      type: 'system',
      icon: 'left',
      message: `${user.pseudonym} a quitté le salon de discussion`
    })
  }

  message_in_catch_up ({ teacher }) {
    this.store.commit('server/set_teacher', teacher)
  }

  message_in_register_teacher_reply ({ accepted }) {
    this.store.commit('server/set_teacher', accepted)

    if (accepted) {
      Snackbar.open({
        message: 'Vous avez désormais accès au mode encadrant !',
        duration: 6000
      })
    } else {
      Snackbar.open({
        message: 'Le mot de passe d\'accès au mode encadrant était incorrect.<br />Veuillez réessayer.',
        duration: 6000,
        type: 'is-danger'
      })
    }
  }

  message_in_set_teacher ({ uuid, teacher }) {
    this.store.commit('server/set_user_teacher', { uuid, teacher })
  }

  message_in_set_pseudonym ({ uuid, pseudonym }) {
    const user = this.store.state.server.users[uuid]
    const old_pseudonym = user ? user.pseudonym : '<unknown>'

    this.store.commit('server/set_user_pseudonym', { uuid, pseudonym })

    this.store.commit('chat/add_chat', {
      channel: 'global',
      type: 'system',
      icon: 'pseudonym',
      message: `${old_pseudonym} s'appelle désormais ${pseudonym}`
    })
  }

  message_in_chat ({ uuid, message, channel }) {
    channel = channel || 'global'

    this.store.commit('chat/add_chat', {
      channel,
      type: 'user',
      author: uuid,
      message: md.renderInline(message)
    })

    if (this.store.state.chat.focused !== channel) {
      this.store.commit('chat/increment_unread_count', channel)
    }
  }

  send_pseudonym_change (pseudonym) {
    return this.send_message('change-pseudonym', { pseudonym })
  }

  send_teacher_request (password) {
    return this.send_message('register-teacher', { password })
  }

  send_chat_message (channel, message) {
    return this.send_message('chat', { channel, message })
  }
}
