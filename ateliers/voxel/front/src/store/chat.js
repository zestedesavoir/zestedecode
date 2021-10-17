import Vue from 'vue'

const short_date_format = new Intl.DateTimeFormat('fr-FR', {
  hour: 'numeric',
  minute: 'numeric'
})

const long_date_format = new Intl.DateTimeFormat('fr-FR', {
  weekday: 'long',
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  hour: 'numeric',
  minute: 'numeric',
  second: 'numeric'
})

/**
 * Server-related informations like connection status,
 * ping, other participants, …
 */
export default client => ({
  namespaced: true,

  state: {
    /**
     * Chat logs are stored here. The key is the channel, and the
     * value, a list of chat message objects with the following keys:
     * - type ('system' or 'user');
     * - icon (for system messages only) ('join', 'left' or 'pseudonym');
     * - author (for user messages only) (an UUID);
     * - message (the message's content; HTML allowed).
     *
     * A `date` object is automatically added to the message object, with
     * two keys in it:
     * - short (the message's date, rendered as a short date, only the hours & minutes);
     * - long (the message's date, rendered as a full date with everything).
     *
     * The main channel is called “global”.
     */
    logs: {},

    /**
     * For each channel, stores the unread count.
     */
    unread: {},

    /**
     * Stores the currently-focused channel, so we don't display unread
     * notifications for the channel we're looking at.
     */
    focused: null
  },

  mutations: {
    add_chat (state, { channel, ...message }) {
      const now = new Date()

      let channel_log = state.logs[channel]

      if (!channel_log) {
        channel_log = []
        Vue.set(state.logs, channel, channel_log)
      }

      channel_log.push({
        ...message,
        date: {
          short: short_date_format.format(now),
          long: long_date_format.format(now)
        }
      })
    },

    set_focused_channel (state, channel) {
      state.focused = channel
    },

    increment_unread_count (state, channel) {
      if (!state.unread[channel]) {
        Vue.set(state.unread, channel, 1)
      } else {
        state.unread[channel]++
      }
    },

    mark_channel_as_read (state, channel) {
      Vue.set(state.unread, channel, 0)
    }
  },

  actions: {
    send_chat_message (_, { channel, message }) {
      client.send_chat_message(channel, message)
    }
  }
})
