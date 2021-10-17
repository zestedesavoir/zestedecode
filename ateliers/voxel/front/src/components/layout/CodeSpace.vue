<template>
    <main id="code-space">
        <div class="code-space-content">
            <ide />

            <section class="game">
              <b-tabs class="block" @input="tab_changed" :animated="false">
                <b-tab-item label="Jeu" value="game" icon="cubes">
                  <b-skeleton height="100%"></b-skeleton>
                </b-tab-item>
                <b-tab-item label="Chat" value="chat-global" icon="comment-dots" icon-pack="far">
                  <template slot="header">
                    <b-icon icon="comment-dots" pack="far" />
                    <span>Chat <b-tag rounded type="is-accent" v-show="unread_count_global !== 0">{{ unread_count_global }}</b-tag></span>
                  </template>
                  <chat channel="global">
                    <h3 class="title is-5">
                      Discutez avec les autres participants
                    </h3>
                  </chat>
                </b-tab-item>
                <b-tab-item label="Recevoir de l'aide" :value="`chat-${help_channel_id}`" icon="hands-helping" :disabled="!uuid">
                  <chat :channel="help_channel_id">
                    <div class="level">
                      <div class="level-left">
                        <div class="level-item title is-5">
                          Discussion privée avec les organisateurs
                        </div>
                      </div>
                      <div class="level-right">
                        <div class="level-item"><online :online="teachers_online > 0" /></div>
                        <div class="level-item">{{ teachers_online > 0 ? teachers_online : 'Aucun' }} organisateur{{ teachers_online > 1 ? 's' : '' }} en ligne</div>
                      </div>
                    </div>
                  </chat>
                </b-tab-item>
              </b-tabs>
            </section>
        </div>
    </main>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

import Chat from '../sections/Chat'
import Ide from '../sections/Ide'

import Online from '../elements/Online'

export default {
  computed: {
    ...mapState('server', ['uuid', 'users']),
    ...mapState('chat', {
      unread_count: state => state.unread,
      focused_channel: state => state.focused,
      chat_logs: state => state.logs
    }),

    help_channel_id () {
      return `help:${this.uuid}`
    },

    unread_count_global () {
      return this.unread_count.global || 0
    },

    unread_count_help () {
      return this.unread_count[this.help_channel_id] || 0
    },

    teachers_online () {
      return Object.values(this.users).filter(user => user.teacher && user.online).length
    }
  },

  methods: {
    ...mapMutations('chat', ['add_chat', 'set_focused_channel', 'mark_channel_as_read']),

    tab_changed (tab) {
      if (!tab.startsWith('chat-')) {
        this.set_focused_channel(null)
      } else {
        this.set_focused_channel(tab.slice(5))
      }
    }
  },

  watch: {
    focused_channel () {
      if (this.focused_channel) {
        this.mark_channel_as_read(this.focused_channel)
      }
    },

    uuid () {
      if (this.uuid !== null && !this.chat_logs[this.help_channel_id]) {
        this.add_chat({
          channel: this.help_channel_id,
          type: 'notification',
          title: 'Bienvenue dans votre espace d\'aide privé !',
          message: `Cet espace vous permet de discuter en privé avec tous les organisateurs de Zeste de Code.
                    Besoin d'aide ? Quelque chose que vous avez mal compris ou mal entendu ? N'hésitez pas,
                    nous répondrons !<br />Et n'oubliez pas : il n'y a pas de questions bêtes.`
        })
      }
    }
  },

  components: {
    Chat,
    Ide,
    Online
  }
}
</script>

<style lang="sass">
@import "@/assets/main"

main#code-space
  height: 100%

  .code-space-content
    display: flex
    flex-direction: row

    padding: $length-10

    height: 100%

    > section
      width: 50%
      margin: 0

      &.game
        .b-tabs
          display: flex
          flex-direction: column-reverse
          height: 100%

          .tabs
            ul
              border-top: solid $length-1 $grey-100
              border-bottom: none

              li a
                border-bottom: none
                border-top: solid $length-1 $grey-100

                &:hover, &:active
                  border-top-color: $grey-800

                .tag
                  margin-left: $length-4

                  padding-left: $length-6
                  padding-right: $length-6

                  height: $length-12

                  font-size: .8rem
                  font-weight: bold

              li.is-active a
                border-top-color: $accent-800
                color: $accent-800

          .tab-content
            flex: 21
            padding: 0 0 $length-10 0

            .tab-item
              height: 100%
</style>
