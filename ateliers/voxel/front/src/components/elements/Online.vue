<template>
  <span
    class="online-dot"
    :class="{'is-online': online}"
    :title="online ? 'Connecté⋅e' : 'Hors-ligne'"
    :aria-label="online ? 'Connecté⋅e' : 'Hors-ligne'" />
</template>

<script>
export default {
  props: {
    online: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="sass">
@import "@/assets/main"

.online-dot
  --color-dot: #{$grey-200}
  --color-shadow: #{rgba($grey-400, .4)}

  display: inline-block
  width: 8px
  height: 8px
  border-radius: $radius-round
  background-color: var(--color-dot)
  box-shadow: 0 0 10px var(--color-shadow)

  &.is-online
    --color-dot: #{$green-600}
    --color-shadow: #{rgba($green-500, .9)}
</style>
