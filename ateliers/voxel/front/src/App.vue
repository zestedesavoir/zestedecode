<template>
  <div id="app">
    <app-header />
    <code-space />
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue'
import CodeSpace from './components/CodeSpace.vue'

export default {
  name: 'App',
  components: {
    AppHeader,
    CodeSpace
  }
}
</script>

<style lang="sass">
@import "assets/main"

body
  height: 100vh

#app
  display: flex
  flex-direction: column

  margin: 0
  padding: 0

  height: 100%

  > header
    height: 3.2rem
    user-select: none

  > main
    flex: 12
</style>
