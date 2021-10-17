import crypto from "crypto"

import fs from "fs"
import path from "path"

import { v4 as uuidv4 } from "uuid"
import { server as WebSocketServer } from "websocket"

// import { Munin } from "munin-http"

import { Game } from "./game"
import { log_info, log_err, log_debug } from "./logging"

export default class ZestVoxelServer {
  constructor(http_server) {
    this.http_server = http_server

    this.clients = {}
    this.clients_connections = {}
    this.clients_secrets = {}

    this.clients_logged_out_at = {}
    this.client_forget_threshold = 1000 * 60 * 60 * 2

    this.chat = {
      logs: {},
      unreads: {}
    }

    // this.setup_munin()
  }

  /**
   * Sets the password teachers will have to use to enable teacher mode.
   * @param {String} teachers_password The password.
   */
  set_teachers_password(teachers_password) {
    this.teachers_password = teachers_password
  }

  /**
  * Sets-up Munin data reporting.
  * TODO
  */
  setup_munin() {
    this.munin = new Munin(this.http_server, "/munin")

    this.munin.add_source("clients", {
      "config": {
        "graph_title": "Connected clients",
        "graph_info": "Number of users with an active connection to the websockets server.",
        "graph_vlabel": "Clients",
        "graph_category": "zeste_de_code_voxel"
      },
      "data": {
        "clients": {
          "label": "Connected clients",
          "warning": 1000,
          "critical": 1024,
          "value": () => Object.keys(this.clients_connections).length
        }
      }
    })

    this.munin.add_source("players", {
      "config": {
        "graph_title": "Connected players",
        "graph_info": "Number of players connected to the actual game.",
        "graph_vlabel": "Amount",
        "graph_category": "zeste_de_code_voxel"
      },
      "data": {
        "players": {
          "label": "Players (non-unique)",
          "value": () => this.statistics["players"] || 0
        },
      }
    })
  }

  static check_origin(origin) {
    if (!process.env.ALLOWED_ORIGIN) return true
    return origin.toLowerCase() === process.env.ALLOWED_ORIGIN
  }

  /**
  * Starts the websocket server and registers all its listeners.
  */
  async start() {
    this.ws_server = new WebSocketServer({
      httpServer: this.http_server,
      autoAcceptConnections: false
    })

    log_info("Zeste de Code websocket server started.")

    this.ws_server.on('request', request => {
      if (!ZestVoxelServer.check_origin(request.origin)) {
        request.reject()
        log_err(`Connection from origin ${request.origin} rejected.`)
        return
      }

      const connection = request.accept('zdc-voxel-protocol', request.origin)
      let first_uuid_message = true

      connection.on('message', message => {
        if (message.type === 'utf8') {
          // Handle ping messages immediately without further processing
          if (message.utf8Data.startsWith('ping!')) {
            connection.sendUTF(`pong!${message.utf8Data.slice(5)}`)
            return
          }

          let json_message = JSON.parse(message.utf8Data)

          if (json_message.action != 'ping') {
            log_debug(() => `[<- ${connection.socket._peername.port}] ${message.utf8Data}`)
          }

          let uuid = (json_message.uuid || "").toString().toLowerCase().trim()
          let action = (json_message.action || "").toString().toLowerCase().trim()

          if (!action) {
            log_debug("Ignoring action-less message from " + (uuid || "an unknown client") + ".")
            return
          }

          let uuid_promise = null

          // If the user does not have an UUID, we generate one.
          // We also generate one if we don't know this UUID (without
          // this, if we stay on a tab when the server restarts, we
          // are unable to connect from this tab).
          if (!uuid || (!this.clients_connections[uuid]) && !this.clients_secrets[uuid]) {
            uuid = uuidv4().toLowerCase()
            let secret = crypto.randomBytes(16).toString("hex")

            this.clients_secrets[uuid] = secret

            uuid_promise = this.send_message(connection, "set-uuid", {uuid: uuid, secret: secret})
          }

          // Else we check the secret.
          else {
            if ((this.clients_secrets[uuid] || "") !== (json_message.secret || "").trim()) {
              log_err(`Client with UUID ${uuid} sent a badly authenticated message. Ignored.`)
              log_err(`Server secret: ${this.clients_secrets[uuid] || "(empty)"}`)
              log_err(`Client secret: ${json_message.secret || "(empty)"}`)
              this.send_message(connection, "invalid-secret", {})
              return
            }
          }

          // If there is a client already connected with the same UUID,
          // we disconnect the old one with a message (that means the
          // user joined in another tab).
          if (first_uuid_message && this.clients_connections[uuid]) {
            this.send_message(this.clients_connections[uuid], 'connected-from-another-tab').then(() => {
              this.clients_connections[uuid].close()
            })
          }

          first_uuid_message = false

          if (!this.clients_connections[uuid]) {
            this.clients_connections[uuid] = connection
          }

          (uuid_promise || Promise.resolve()).then(() => {
            if (this.clients_logged_out_at[uuid]) {
              delete this.clients_logged_out_at[uuid]
            }

            this.handle_message(connection, uuid, action, json_message)
          })
        }
      })

      connection.on('close', (reasonCode, description) => {
        // We DON'T remove the client' secret to allow for reconnection
        // using the same UUID/secret.
        let uuid = this.get_uuid_for_connection(connection)
        let client = this.clients[uuid]

        if (client) {
          client.online = false
        }

        delete this.clients_connections[uuid]
        this.broadcast_message('user-left', { uuid })

        log_info(`User ${client ? client.pseudonym : '<unknown>'} (${uuid}) left`)
      })
    })
  }

  get_connection_for_uuid(uuid) {
    return this.clients_connections[uuid]
  }

  get_uuid_for_connection(connection) {
    return Object.keys(this.clients_connections).filter(client_uuid => this.clients_connections[client_uuid] === connection)[0]
  }

  send_message(connection, action, message) {
    return new Promise((resolve, reject) => {
      message = message || {}
      message.action = action

      let raw_message = JSON.stringify(message)

      connection.sendUTF(raw_message)

      if (action != 'pong') {
        log_debug(() => `[-> ${connection.socket._peername.port}] ${raw_message}`)
      }

      resolve()
    })
  }

  broadcast_message(action, message, filter_fn) {
    return Promise.all(Object.keys(this.clients_connections)
    .filter(client_uuid => filter_fn ? filter_fn(client_uuid) : true)
    .map(client_uuid => this.clients_connections[client_uuid])
    .map(connection => this.send_message(connection, action, message))
    )
  }

  /**
  * Internal method to handle an incoming message and call the appropriate
  * method.
  *
  * @param {string} action The incoming message's action.
  * @param {object} message The received payload.
  */
  handle_message (connection, uuid, action, message) {
    const method_name = 'message_in_' + action.replace(/-/g, '_').trim().toLowerCase()

    if (typeof this[method_name] === 'function') {
      this[method_name](connection, uuid, message)
    }
  }

  /**
   * The initial connection of a client. We create a new client profile and
   * broadcast a join message. We also broadcast join messages from all already
   * connected users to the new one.
   */
  message_in_handshake(connection, uuid, { pseudonym }) {
    if (this.clients[uuid]) {
      this.clients[uuid].pseudonym = pseudonym
      this.clients[uuid].online = true
    } else {
      this.clients[uuid] = {
        uuid,
        pseudonym: pseudonym,
        teacher: false,
        online: true,
        code: ''
      }
    }

    const teacher = this.clients[uuid].teacher

    this.broadcast_message('user-join', {
      uuid,
      pseudonym,
      online: true,
      teacher,
      realtime: true
    })

    Object.values(this.clients)
      .filter(client => client.uuid !== uuid)
      .forEach(client => this.send_message(connection, 'user-join', {
        uuid: client.uuid,
        pseudonym: client.pseudonym,
        teacher: client.teacher,
        online: client.online,
        realtime: false
      }))

    if (teacher) {
      this.send_message(connection, 'catch-up', {
        teacher: true
      })
    }

    log_info(`User ${pseudonym} joined with UUID ${uuid}`)
  }

  message_in_chat(connection, uuid, { channel, message }) {
    let log = this.chat.logs[channel]
    if (!log) {
      log = []
      this.chat.logs[channel] = log
    }

    log.push({
      uuid,
      message: message.toString(),
      date: new Date()
    })

    this.broadcast_message(
      'chat', { uuid, channel, message },
      target_uuid => channel === 'global' ? true : uuid === target_uuid || this.clients[target_uuid].teacher)
  }

  message_in_change_pseudonym(connection, uuid, { pseudonym }) {
    const client = this.clients[uuid]
    if (!client) return

    client.pseudonym = pseudonym
    this.broadcast_message('set-pseudonym', { uuid, pseudonym })
  }

  message_in_register_teacher(connection, uuid, { password }) {
    const client = this.clients[uuid]
    if (!client) return

    if (password === this.teachers_password) {
      client.teacher = true
      this.send_message(connection, 'register-teacher-reply', {
        accepted: true
      })
      this.broadcast_message('set-teacher', { uuid, teacher: true })
    } else {
      this.send_message(connection, 'register-teacher-reply', {
        accepted: false
      })
    }
  }
}
