<template>
  <section class="chat-log">
    <header>
      <slot />
    </header>
    <article ref="log_container">
      <div class="media"
           v-for="(chat, i) in log" :key="i"
           :class="{
             'is-system-message': chat.type === 'system',
             'is-notification-message': chat.type === 'notification',
             'is-same-author': i > 0 ? log[i-1].author === chat.author : false,
             'is-teacher': chat.author && chat.author.teacher
            }">
        <figure class="media-left" v-if="chat.type === 'system'" aria-hidden="true">
          <b-icon icon="arrow-right" v-if="chat.icon === 'join'" />
          <b-icon icon="arrow-left" v-if="chat.icon === 'left'" />
          <b-icon icon="signature" v-if="chat.icon === 'pseudonym'" />
        </figure>

        <div class="media-content">
          <template v-if="chat.type !== 'notification'">
            <header v-if="chat.type !== 'system'">
              <b-icon icon="chalkboard-teacher" size="is-small" v-if="chat.author.teacher" title="Organisateur" />
              <strong>{{ chat.author.pseudonym }}</strong>
              <b-tooltip :label="chat.date.long" position="is-right" type="is-dark">
                <small>{{ chat.date.short }}</small>
              </b-tooltip>
            </header>

            <div class="content">
              <p v-html="chat.message" />
            </div>
          </template>
          <b-notification type="is-primary is-light" role="alert" :closable="false" v-else>
            <h4>{{ chat.title }}</h4>

            <div class="content">
              <p v-html="chat.message" />
            </div>
          </b-notification>
        </div>
      </div>
    </article>
    <footer>
      <b-input
        extended
        placeholder="Envoyer un message…"
        icon-pack="fab"
        icon-right="markdown"
        v-model="message"
        @keyup.enter.native="send_message" />
    </footer>
  </section>
</template>

<script>
import Vue from 'vue'
import { mapState, mapActions } from 'vuex'

export default {
  props: {
    channel: {
      type: String
    }
  },

  data () {
    return {
      message: ''
    }
  },

  computed: {
    ...mapState('server', ['users']),
    ...mapState('chat', {
      chat_logs: state => state.logs
    }),

    log () {
      if (!this.chat_logs[this.channel]) return []

      return this.chat_logs[this.channel]
        .map(log => ({ ...log, author: this.users[log.author] || { pseudonym: 'Participant inconnu', teacher: false } }))
    },

    are_we_focused () {
      return this.chat_logs.focused === this.channel
    }
  },

  methods: {
    ...mapActions('chat', ['send_chat_message']),

    send_message () {
      this.send_chat_message({
        channel: this.channel,
        message: this.message
      })

      this.message = ''
    },

    scroll_down () {
      Vue.nextTick(() => {
        this.$refs.log_container.scrollTop = this.$refs.log_container.scrollHeight
      })
    }
  },

  watch: {
    log () {
      this.scroll_down()
    },

    are_we_focused () {
      if (this.are_we_focused) {
        this.scroll_down()
      }
    }
  },

  mounted () {
    this.scroll_down()
  }
}
</script>

<style lang="sass">
@import '@/assets/main'

section.chat-log
  position: relative

  display: flex
  flex-direction: column

  height: 100%

  > header
    height: $length-24
    color: $grey-500
    user-select: none

    .title
      color: $grey-800

  > article
    flex: 21

    margin-bottom: $length-16
    padding-left: $length-4

    height: calc(100vh - 248px)
    max-height: calc(100vh - 248px)

    overflow-x: hidden

    .media
      &.is-system-message
        align-items: center
        user-select: none

        figure, .content
          margin-top: 0
          color: $grey-500

      &.is-notification-message
        border-top: none
        user-select: none

        & + .media
          margin-top: 0
          border-top: none

      &.is-same-author
        margin-top: 0
        padding-top: 0
        border-top: none

        header
          display: none

      &.is-teacher
        header
          .icon
            margin-right: $length-4
            color: $accent-700

          strong
            color: $accent-800

      header
        display: flex
        align-items: center

        color: $grey-700
        cursor: default

        small
          color: $grey-400
          margin: 0 $length-4

      .content
        margin-top: $length-2
        color: $grey-900

        code
          color: $primary-900
          background: $grey-100
          border-radius: $radius-1
          padding: 0 $length-4

      .notification
        &, .content p
          color: $primary-700

        h4
          font-weight: bold
</style>
