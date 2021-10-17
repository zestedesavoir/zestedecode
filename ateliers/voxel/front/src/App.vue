<template>
  <div id="app">
    <b-loading is-full-page v-model="loading">
      <div class="bounce-loader" :aria-label="loading_message ? '' : 'Chargement en cours…'" :aria-hidden="!!loading_message" v-if="loading_display_loader">
        <div /><div />
      </div>
      <p v-if="loading_message" v-html="loading_message" />
    </b-loading>

    <app-header @show-welcome-screen="display_welcome = true" />
    <code-space :class="{'is-blurred': display_welcome || loading }" />

    <b-modal
      v-model="display_welcome"
      trap-focus
      :can-cancel="!first_welcome"
      :destroy-on-hide="true"
      width="100%"
      aria-role="dialog"
      aria-modal>
      <template #default="props">
          <welcome :first="first_welcome" @close="props.close" />
      </template>
    </b-modal>
  </div>
</template>

<script>
import AppHeader from './components/layout/AppHeader.vue'
import CodeSpace from './components/layout/CodeSpace.vue'

import Welcome from './components/layout/Welcome.vue'

import { mapState, mapActions } from 'vuex'

export default {
  data () {
    return {
      display_welcome: false,
      first_welcome: true
    }
  },

  computed: {
    ...mapState({
      pseudonym: state => state.server.pseudonym,
      loading: state => state.loading.active,
      loading_message: state => state.loading.message,
      loading_display_loader: state => state.loading.loader
    })
  },

  methods: mapActions('server', ['set_pseudonym_and_connect']),

  mounted () {
    // If the pseudonym is not set in the local storage, it's the first time
    // the user join the website and we display the welcome screen.
    // Also, if the user joined on an old workshop, we display the welcome
    // screen again.

    const ls_pseudonym = localStorage.getItem('zestedecode-voxel-pseudonym')
    const ls_version = localStorage.getItem('zestedecode-voxel-version')

    if (!ls_pseudonym || ls_version !== process.env.VUE_APP_WORKSHOP_VERSION) {
      this.display_welcome = true
    } else {
      this.first_welcome = false
      this.set_pseudonym_and_connect(ls_pseudonym)
    }

    localStorage.setItem('zestedecode-voxel-version', process.env.VUE_APP_WORKSHOP_VERSION)
  },

  watch: {
    pseudonym () {
      if (this.pseudonym) {
        this.display_welcome = false
        this.first_welcome = false
      }
    }
  },

  components: {
    AppHeader,
    CodeSpace,
    Welcome
  }
}
</script>

<style lang="sass">
@import "assets/main"

html, body
  height: 100vh
  overflow: hidden

#app
  display: flex
  flex-direction: column

  margin: 0
  padding: 0

  height: 100%

  > header
    height: $length-32
    user-select: none

  > main
    flex: 12

    &.is-blurred
      filter: blur(4px)

  .loading-overlay
    display: flex
    flex-direction: column
    align-items: center

    .bounce-loader
      position: relative

      width: $length-48
      height: $length-48

      > div
        position: absolute
        top: 0
        left: 0

        width: 100%
        height: 100%
        border-radius: 50%

        background-color: $grey-600

        opacity: .4

        animation: bounce 2s infinite ease-in-out

        &:last-child
          animation-delay: -1s;

    p
      margin-top: $length-16

      font-family: $family-sans-serif
      font-size: $length-24
      font-weight: 300

      color: $grey-900
      text-align: center

      small
        font-size: $length-16

  input.input::placeholder
    color: $grey-800

@keyframes bounce
  0%, 100%
    transform: scale(0.0)
  50%
    transform: scale(1.0)
</style>
