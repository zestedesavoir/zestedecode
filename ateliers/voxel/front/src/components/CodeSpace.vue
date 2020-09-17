<template>
    <main id="code-space">
        <div class="code-space-content">
            <section class="ide">
                <header>
                  <div class="titles">
                    <h2 class="title">Votre code</h2>
                    <p class="subtitle">Tout ce que vous écrirez ici contrôlera votre personnage</p>
                  </div>
                  <aside>
                    <b-tooltip label="Ctrl + Entrée" type="is-white" position="is-bottom">
                      <b-button type="is-success" icon-left="play" @click="exec_code">Lancer</b-button>
                    </b-tooltip>
                  </aside>
                </header>

                <article>
                  <codemirror v-model="code" @ready="on_ide_ready" @input="save_code" />
                  <footer>
                    <p v-if="errors.length === 0">Sauvegardé automatiquement dans votre navigateur</p>
                    <p v-else class="has-errors is-error-message">
                      <b-tooltip
                        v-if="error.type === 'SyntaxError'"
                        label="Erreur de syntaxe : peut-être une faute de frappe ?"
                        type="is-danger"
                        position="is-right"
                        multilined>
                        <b-icon size="is-small" icon="keyboard" pack="far" />
                      </b-tooltip>
                      <b-tooltip
                        v-else
                        label="Erreur pendant l'exécution du code"
                        type="is-danger"
                        position="is-right"
                        multilined>
                        <b-icon size="is-small" icon="bug" />
                      </b-tooltip>
                      <span>{{ error.type }}: {{ error.message }}</span>
                    </p>

                    <p v-if="errors.length === 0">Aucune erreur</p>
                    <p v-else class="has-errors">{{ errors.length === 1 ? 'Une' : errors.length }} erreur{{ errors.length > 1 ? 's' : '' }}</p>
                  </footer>
                </article>
            </section>

            <section class="game">
              <b-tabs size="is-" class="block">
                <b-tab-item label="Jeu" icon="cubes">
                  <b-skeleton height="100%"></b-skeleton>
                </b-tab-item>
                <b-tab-item label="Chat" icon="comment-dots" icon-pack="far"></b-tab-item>
                <b-tab-item label="Recevoir de l'aide" icon="hands-helping"></b-tab-item>
              </b-tabs>
            </section>
        </div>
    </main>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'

export default {
  data: function () {
    return {
      code: '',
      ide: null
    }
  },

  computed: {
    ...mapState({
      state_code: state => state.ide.code,
      errors: state => state.ide.errors
    }),

    error () {
      return this.errors[this.errors.length - 1]
    }
  },

  methods: {
    ...mapMutations(['set_code']),
    ...mapActions(['exec_code']),

    on_ide_ready (cm) {
      this.ide = cm

      this.ide.setOption('extraKeys', {
        'Ctrl-Enter': cm => {
          this.exec_code()
        }
      })
    },

    save_code () {
      this.set_code(this.code)
      localStorage.setItem('zestedecode-voxel-source-code', this.code)
    }
  },

  watch: {
    errors () {
      // On errors change, we update the errors inside the CodeMirror IDE
      // First we clear out all errors
      for (const line of this.ide.display.lineSpace.querySelectorAll('.CodeMirror-code > div')) {
        line.classList.remove('has-error')
      }

      // Then we add the new ones, if any
      for (const error of this.errors) {
        if (!error.lineNumber) continue
        const errored_line = this.ide.display.lineSpace.querySelector(`.CodeMirror-code > div:nth-child(${error.lineNumber})`)

        if (errored_line) {
          errored_line.classList.add('has-error')
        }
      }
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
  }
}
</script>

<style lang="sass">
@import "../assets/main"

main#code-space
  height: 100%

  .code-space-content
    display: flex
    flex-direction: row

    padding: 1rem

    height: 100%

    > section
      width: 50%
      margin: 0

      &.ide
        padding-right: 1rem

        header
          display: flex
          align-items: flex-start

          margin-bottom: 1.5rem

          .titles
            flex: 2

          .button.is-success
            font-weight: bold

        article
          height: calc(100vh - 200px)
          // max-height: calc(100vh - 120px)

          .vue-codemirror
            height: 100%

            border: solid 1px hsl(214, 15%, 91%)
            border-bottom: dashed 1px hsl(214, 15%, 91%)

            border-radius: 6px
            border-bottom-left-radius: 0
            border-bottom-right-radius: 0

            cursor: text

            .CodeMirror
              height: 100%
              border-radius: 6px

              .CodeMirror-selected
                background-color: hsl(198, 40%, 87%)

              .CodeMirror-code
                .has-error
                  .CodeMirror-linenumber
                    color: hsl(360, 72%, 38%)
                    font-weight: bold

                  .CodeMirror-line
                    background-color: hsl(360, 82%, 89%)

                    span[role="presentation"]
                      .has-error
                        border-bottom: dotted 2px hsl(360, 72%, 38%)

              .CodeMirror-gutter
                cursor: default

          footer
            display: flex
            align-items: center

            height: 1.6rem

            padding: 0 .4rem

            border: solid 1px hsl(214, 15%, 91%)
            border-top: none

            border-radius: 6px
            border-top-left-radius: 0
            border-top-right-radius: 0

            background-color: white

            user-select: none
            cursor: default

            p
              font-size: .8rem
              color: hsl(211, 12%, 43%)

              &:first-child
                flex: 12

              &.has-errors
                display: inline-flex
                align-items: center

                color: hsl(360, 72%, 38%)

                &.is-error-message
                  font-family: $family-monospace
                  user-select: all
                  cursor: text

                .b-tooltip
                  margin-right: .2rem
                  height: 16px
                  cursor: help

      &.game
        .b-tabs
          display: flex
          flex-direction: column-reverse
          height: 100%

          .tabs
            ul
              border-top: solid 1px hsl(214, 15%, 91%)
              border-bottom: none

              li a
                border-bottom: none
                border-top: solid 1px hsl(214, 15%, 91%)

                &:hover, &:active
                  border-top-color: hsl(209, 20%, 25%)

              li.is-active a
                border-top-color: hsl(22.1, 81.9%, 39%)

          .tab-content
            flex: 21
            padding: 0 0 1rem 0
</style>
