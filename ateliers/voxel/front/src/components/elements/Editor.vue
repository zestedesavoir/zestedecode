<template>
  <article class="ide-editor">
    <codemirror
      v-model="code"
      v-on="$listeners"
      :options="codemirror_options"
      @ready="on_ide_ready" />

    <footer>
      <p v-if="readonly && errors.length === 0">Lecture seule</p>
      <p v-else-if="success" class="is-success-message">
        <b-icon size="is-small" icon="check-circle" />
        Code exécuté avec succès
      </p>
      <p v-else-if="errors.length === 0">Sauvegardé automatiquement dans votre navigateur</p>
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

      <p v-if="errors.length === 0 && !readonly">Aucune erreur</p>
      <p v-else-if="errors.length > 0" class="has-errors">{{ errors.length === 1 ? 'Une' : errors.length }} erreur{{ errors.length > 1 ? 's' : '' }}</p>
    </footer>
  </article>
</template>

<script>
import Vue from 'vue'

export default {
  model: {
    prop: 'value',
    event: 'input'
  },

  props: {
    /**
     * The code itself. You should use v-model for bi-directional sync.
     */
    value: {
      type: String,
      default: ''
    },

    /**
     * An array of error objects to display, if any. Corresponding lines
     * will be highlighted and the first error will be displayed at the
     * bottom of the editor.
     *
     * Required keys for each array entry:
     * - lineNumber
     * - type
     * - message
     */
    errors: {
      type: Array,
      default: () => []
    },

    /**
     * If true, the footer will display that the code was successfully
     * executed.
     */
    success: {
      type: Boolean,
      default: false
    },

    /**
     * If true, the editor will be readonly and the footer will warn the
     * user about that.
     */
    readonly: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      code: '',
      ide: null
    }
  },

  computed: {
    error () {
      return this.errors[this.errors.length - 1]
    },

    codemirror_options () {
      return {
        readOnly: this.readonly
      }
    }
  },

  methods: {
    on_ide_ready (cm) {
      this.ide = cm

      this.ide.setOption('extraKeys', {
        'Ctrl-Enter': cm => {
          this.$emit('exec')
        }
      })
    },

    display_errors_on_editor () {
      Vue.nextTick(() => {
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
      })
    }
  },

  watch: {
    errors () {
      // On errors change, we update the errors inside the CodeMirror IDE
      this.display_errors_on_editor()
    }
  },

  mounted () {
    Vue.nextTick(() => {
      this.code = this.value
      this.display_errors_on_editor()
    })
  }
}
</script>

<style lang="sass">
@import '@/assets/main'

article.ide-editor
  .vue-codemirror
    height: 100%

    border: solid $length-1 $grey-100
    border-bottom: dashed $length-1 $grey-100

    border-radius: $radius-1
    border-bottom-left-radius: 0
    border-bottom-right-radius: 0

    cursor: text

    .CodeMirror
      height: 100%

      border-radius: $radius-1
      border-bottom-left-radius: 0
      border-bottom-right-radius: 0

      .CodeMirror-selected
        background-color: $primary-000

      .CodeMirror-code
        .has-error
          .CodeMirror-linenumber
            color: $red-600
            font-weight: bold

          .CodeMirror-line
            background-color: $red-100

            span[role="presentation"]
              .has-error
                border-bottom: dotted $length-2 $red-600

      .CodeMirror-gutter
        cursor: default

  footer
    display: flex
    align-items: center

    height: $length-16

    padding: 0 $length-4

    border: solid $length-1 $grey-100
    border-top: none

    border-radius: $radius-1
    border-top-left-radius: 0
    border-top-right-radius: 0

    background-color: white

    user-select: none
    cursor: default

    p
      font-size: .8rem
      color: $grey-500

      &:first-child
        flex: 12

      &.is-success-message
        display: flex
        align-items: center

        font-family: $family-monospace
        color: $green-700

        span.icon
          margin-right: $length-4

      &.has-errors
        display: inline-flex
        align-items: center

        color: $red-600

        &.is-error-message
          font-family: $family-monospace
          user-select: all
          cursor: text

        .b-tooltip
          margin-right: $length-2
          height: 16px
          cursor: help
</style>
