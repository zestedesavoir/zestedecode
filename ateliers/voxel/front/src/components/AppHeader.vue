<template>
  <header>
    <div class="head">
      Zeste de Code
    </div>
    <div class="zds">
      <a href="https://zestedesavoir.com" target="_blank">
        Une initiative de
        <img src="../assets/zestedesavoir.svg" alt="Zeste de Savoir" />
      </a>
    </div>

    <div class="status" :class="{'is-error': server_status !== 'CONNECTED', 'is-warning': bad_connection }">
      <template v-if="server_status === 'CONNECTED' && !bad_connection">
        <b-icon pack="far" icon="check-circle" />
        <p>Connecté⋅e</p>
      </template>
      <template v-else-if="bad_connection">
        <b-icon icon="exclamation-circle" />
        <p>Connexion mauvaise</p>
      </template>
      <template v-else>
        <b-icon icon="exclamation-circle" />
        <p>Déconnecté⋅e</p>
      </template>
    </div>

    <div class="display-setting">
      <!-- <b-field>
        <p class="control">
          <b-tooltip label="Côte à côte"
            type="is-dark"
            position="is-bottom">
            <button
              class="button is-small is-white"
              :class="{'is-outlined': display === 'COLUMNS', 'is-active': display === 'COLUMNS'}"
              @click="change_display('COLUMNS')">
              <b-icon icon="columns"></b-icon>
            </button>
          </b-tooltip>
        </p>
        <p class="control">
          <b-tooltip label="Plein écran"
            type="is-dark"
            position="is-bottom">
            <button
              class="button is-small is-white"
              :class="{'is-outlined': display === 'FULLSCREEN', 'is-active': display === 'FULLSCREEN'}"
              @click="change_display('FULLSCREEN')">
              <b-icon icon="window-maximize" pack="far"></b-icon>
            </button>
          </b-tooltip>
        </p>
      </b-field> -->

      <b-dropdown v-model="display" aria-role="list" position="is-bottom-left">
        <button class="button is-primary" type="button" slot="trigger">
          <template v-if="display === 'COLUMNS'">
            <b-icon icon="columns"></b-icon>
            <span class="sr-only">Affichage côte à côte</span>
          </template>
          <template v-else>
            <b-icon pack="far" icon="window-maximize"></b-icon>
            <span class="sr-only">Affichage plein écran</span>
          </template>
          <b-icon icon="caret-down"></b-icon>
        </button>

        <b-dropdown-item value="COLUMNS" aria-role="listitem" @click="change_display('COLUMNS')">
          <div class="media">
            <b-icon class="media-left" icon="columns"></b-icon>
            <div class="media-content">
              <h3>Côte à côte</h3>
              <small>Votre code et le jeu sont côte-à-côte</small>
            </div>
          </div>
        </b-dropdown-item>

        <b-dropdown-item value="FULLSCREEN" aria-role="listitem" @click="change_display('FULLSCREEN')">
          <div class="media">
            <b-icon class="media-left" pack="far" icon="window-maximize"></b-icon>
            <div class="media-content">
              <h3>Plein écran</h3>
              <small>Votre code et le jeu sont en plein écran, avec un bouton pour passer de l'un à l'autre</small>
            </div>
          </div>
        </b-dropdown-item>
      </b-dropdown>

    </div>
  </header>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

export default {
  computed: {
    ...mapState({
      server_status: state => state.server.status,
      server_ping: state => state.server.ping,
      display: state => state.display
    }),

    bad_connection () {
      return this.server_ping >= 300
    }
  },

  methods: {
    ...mapMutations(['set_display', 'set_display_active']),

    change_display (display) {
      if (display !== this.display) {
        this.set_display(display)
        if (display !== 'COLUMNS') {
          this.set_display_active('CODE')
        }
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "../assets/main"

header
  display: flex
  align-items: center

  padding: .2rem 1rem

  border-bottom: solid 4px $yellow

  background-color: $primary
  color: $white

  .head
    font-family: $family-monospace
    font-size: 1.4rem

  .zds
    position: relative
    flex: 12

    margin-left: 2rem

    &:before
      content: ''

      position: absolute
      left: -1rem

      display: block

      height: 2rem
      width: 1px

      background-color: rgba(white, .4)

    a
      &, &:hover
        display: inline-flex
        align-items: center

        font-family: $family-sans-serif
        font-size: 1.4rem
        font-weight: 300

        color: white

      img
        display: inline-block
        margin-left: .4rem

        height: 2rem

  .status
    display: flex

    &.is-warning
      color: hsl(29, 80%, 44%)
      font-weight: bold

    &.is-error
      color: hsl(360, 64%, 55%)
      font-weight: bold

    .icon
      margin-right: .4rem

  .display-setting
    margin-left: 1rem
</style>

<style lang="sass">
.display-setting
  .dropdown-menu
    width: 22rem

    .dropdown-item
      white-space: initial !important
</style>
