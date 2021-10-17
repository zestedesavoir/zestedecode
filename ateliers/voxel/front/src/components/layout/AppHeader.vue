<template>
  <header id="app-header">
    <div class="head">
      Zeste de Code
    </div>
    <div class="zds">
      <a href="https://zestedesavoir.com" target="_blank">
        Une initiative de
        <img src="@/assets/zestedesavoir.svg" alt="Zeste de Savoir" />
      </a>
    </div>

    <div class="status" :class="{'is-error': server_status !== 'CONNECTED' && server_status !== 'CONNECTING', 'is-warning': bad_connection }">
      <b-dropdown aria-role="menu" position="is-bottom-left">
        <button class="button is-primary" type="button" slot="trigger" slot-scope="{ active }" @click="check_ctrl_clic_on_user_menu">
          <template v-if="server_status === 'CONNECTING'">
            <b-icon pack="far" icon="dot-circle" />
            <p>Connexion en cours…</p>
          </template>
          <template v-else-if="server_status === 'CONNECTED' && !bad_connection">
            <b-icon pack="far" icon="check-circle" />
            <p>{{ pseudonym }}</p>
          </template>
          <template v-else-if="server_status === 'CONNECTED' && bad_connection">
            <b-icon icon="exclamation-circle" />
            <p>Connexion mauvaise</p>
          </template>
          <template v-else>
            <b-icon icon="exclamation-circle" />
            <p>Déconnecté⋅e</p>
          </template>
          <b-icon :icon="active ? 'caret-up' : 'caret-down'" />
        </button>

        <b-dropdown-item aria-role="menuitem" @click="show_welcome_screen">
          <div class="media">
            <b-icon class="media-left" icon="home"></b-icon>
            <div class="media-content">
              <h3>Afficher l'introduction</h3>
            </div>
          </div>
        </b-dropdown-item>

        <b-dropdown-item aria-role="menuitem" @click="new_psedonym">
          <div class="media">
            <b-icon class="media-left" icon="signature"></b-icon>
            <div class="media-content">
              <h3>Changer de pseudonyme</h3>
              <small>Changer le nom par lequel on vous appelle</small>
            </div>
          </div>
        </b-dropdown-item>

        <b-dropdown-item aria-role="menuitem" @click="activate_teacher" v-if="display_teacher_link && !is_teacher">
          <div class="media">
            <b-icon class="media-left" icon="chalkboard-teacher"></b-icon>
            <div class="media-content">
              <h3>Activer le mode encadrant</h3>
              <small>Accéder aux outils d'aide et de supervision</small>
            </div>
          </div>
        </b-dropdown-item>

        <hr class="dropdown-divider" v-if="server_status === 'CONNECTED'" />

        <b-dropdown-item custom aria-role="menuitem" v-if="server_status === 'CONNECTED'">
          Latence avec le serveur : {{ server_ping }} ms
        </b-dropdown-item>
      </b-dropdown>
    </div>

    <users-list type="is-primary" />
  </header>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'

import UsersList from '../elements/UsersList'

export default {
  data () {
    return {
      display_teacher_link: false
    }
  },

  computed: {
    ...mapState({
      server_status: state => state.server.status,
      server_ping: state => state.server.ping,
      pseudonym: state => state.server.pseudonym,
      is_teacher: state => state.server.teacher
    }),

    bad_connection () {
      return this.server_ping >= 300
    }
  },

  methods: {
    ...mapMutations('display', ['set_display', 'set_display_active']),
    ...mapActions('server', ['change_pseudonym', 'send_teacher_request']),

    new_psedonym () {
      this.$buefy.dialog.prompt({
        message: 'Quel nouveau nom voulez-vous ?',
        inputAttrs: {
          placeholder: 'Entrez un nom…',
          value: this.pseudonym
        },
        trapFocus: true,
        confirmText: 'Changer de nom',
        cancelText: 'Annuler',
        'aria-role': 'dialog',
        'aria-modal': true,
        onConfirm: value => this.change_pseudonym(value)
      })
    },

    check_ctrl_clic_on_user_menu (event) {
      if (event.ctrlKey) {
        this.display_teacher_link = true
      }
    },

    activate_teacher () {
      this.$buefy.dialog.prompt({
        title: 'Mode encadrant',
        message: 'Veuillez entrer le mot de passe du mode encadrant. Vous pourrez ensuite voir les codes des différents participants et répondre aux demandes d\'aide.',
        inputAttrs: {
          placeholder: 'Le mot de passe…',
          type: 'password'
        },
        trapFocus: true,
        hasIcon: true,
        icon: 'chalkboard-teacher',
        confirmText: 'Déverrouiller le mode encadrant',
        cancelText: 'Annuler',
        closeOnConfirm: false,
        'aria-role': 'dialog',
        'aria-modal': true,
        onConfirm: (value, vm) => {
          vm.$refs.confirmButton.classList.add('is-loading')
          this.send_teacher_request(value).then(() => {
            vm.close()
          })
        }
      })
    },

    show_welcome_screen () {
      this.$emit('show-welcome-screen')
    },

    change_display (display) {
      if (display !== this.display) {
        this.set_display(display)
        if (display !== 'COLUMNS') {
          this.set_display_active('CODE')
        }
      }
    }
  },

  components: {
    UsersList
  }
}
</script>

<style lang="sass">
@import "@/assets/main"

header#app-header
  display: flex
  align-items: center

  padding: $length-2 $length-10

  border-bottom: solid 4px $accent-600

  background-color: $primary
  color: $white

  .head
    font-family: $family-monospace
    font-size: 1.4rem

  .zds
    position: relative
    flex: 12

    margin-left: $length-20

    &:before
      content: ''

      position: absolute
      left: -$length-10

      display: block

      height: $length-20
      width: $length-1

      background-color: rgba($white, .4)

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
        margin-left: $length-4

        height: $length-20

  .status
    display: flex

    &.is-warning .dropdown-trigger button
      color: $accent-600
      font-weight: bold

    &.is-error .dropdown-trigger button
      color: $red-400
      font-weight: bold

    .icon:first-of-type
      margin-right: $length-4

  .display-setting
    margin-left: $length-10

    .dropdown-menu
      width: $length-256

      .dropdown-item
        white-space: initial !important
</style>
