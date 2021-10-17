<template>
  <section class="ide">
    <header>
      <div class="titles">
        <h2 class="title">Votre code</h2>
        <p class="subtitle">Tout ce que vous écrirez ici contrôlera votre personnage</p>
      </div>
      <aside>
        <b-tooltip label="Ctrl + Entrée" type="is-white" position="is-bottom">
          <b-button type="is-success" icon-left="play" @click="exec">Lancer</b-button>
        </b-tooltip>
      </aside>
    </header>

    <editor
      v-model="code"
      :success="display_exec_success"
      :errors="errors"
      @input="save_code"
      @exec="exec" />
  </section>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'

import Editor from '../elements/Editor'

export default {
  props: {
    title: {
      type: String,
      default: 'Votre code'
    },
    subtitle: {
      type: String,
      default: 'Tout ce que vous écrirez ici contrôlera votre personnage'
    },
    readonly: {
      type: Boolean,
      default: false
    }
  },

  data: function () {
    return {
      code: '',
      display_exec_success: false,
      display_exec_success_timeout: null
    }
  },

  computed: {
    ...mapState('ide', {
      state_code: state => state.code,
      errors: state => state.errors
    })
  },

  methods: {
    ...mapMutations('ide', ['set_code']),
    ...mapActions('ide', ['exec_code']),

    save_code () {
      this.set_code(this.code)
      localStorage.setItem('zestedecode-voxel-source-code', this.code)
    },

    exec () {
      this.display_exec_success = false

      if (this.display_exec_success_timeout) {
        clearTimeout(this.display_exec_success_timeout)
      }

      this.exec_code().then(() => {
        this.display_exec_success = true
        this.display_exec_success_timeout = setTimeout(() => {
          this.display_exec_success = false
          this.display_exec_success_timeout = null
        }, 4000)
      }).catch(() => {}) // Errors are handled in the store
    }
  },

  mounted () {
    const local_storage_code = localStorage.getItem('zestedecode-voxel-source-code')

    if (local_storage_code) {
      this.code = local_storage_code
      this.save_code()
    } else {
      this.code = this.state_code
    }
  },

  components: {
    Editor
  }
}
</script>

<style lang="sass">
@import "@/assets/main"

section.ide
  padding-right: $length-10

  header
    display: flex
    align-items: flex-start

    margin-bottom: $length-14
    user-select: none

    .titles
      flex: 2

    .button.is-success
      font-weight: bold

  article.ide-editor
    height: calc(100vh - 200px)
</style>
