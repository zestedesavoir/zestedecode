<template>
  <section id="welcome">
    <header class="box">
      <img src="@/assets/zestedesavoir.svg" alt="Zeste de Savoir" />
    </header>

    <div class="box">
      <article>
        <figure aria-hidden="true">
          <b-icon icon="laptop-code" size="is-large" />
        </figure>
        <div>
          <h2>Bienvenue sur Zeste de Code !</h2>
          <p>
            Venez découvrir à quoi ressemble <em>vraiment</em> la programmation et l'informatique,
            en créant vous-même un bout d'un jeu 3D dans le style de Minecraft. Et en multi-joueur !
          </p>
        </div>
      </article>

      <article class="is-link">
         <figure aria-hidden="true">
          <b-icon icon="chalkboard-teacher" size="is-large" />
        </figure>
        <div>
          <h2>N'oubliez pas de suivre la vidéo</h2>
          <p>
            Nous vous expliquons tout en vidéo pendant l'atelier, afin que vous puissiez savoir quoi faire
            et comprendre ce que vous faites.
          </p>
          <p>
            <a href="#" class="button is-link is-outlined" target="_blank">
              <span>Rejoindre sur Twitch</span>
              <b-icon icon="external-link-alt" aria-hidden="true" />
            </a>
          </p>
        </div>
      </article>

      <article v-if="first" class="is-pseudonym-form">
         <figure aria-hidden="true">
          <b-icon icon="signature" size="is-large" />
        </figure>
        <div>
          <h2>Dites-nous juste comment vous appeler</h2>
          <p>
            Cela servira pour le chat et les demandes d'aide, si besoin. Et puis, c'est plus sympa de mettre
            un nom sur quelqu'un !
          </p>
          <b-field>
            <b-input ref="input" placeholder="Entrez un nom…" size="is-medium" expanded v-model="pseudonym" @keydown.enter.native="submit" />
            <p class="control">
              <b-button type="is-primary" size="is-medium" icon-left="angle-right" aria-label="Démarrer" @click="submit" />
            </p>
          </b-field>
        </div>
      </article>
    </div>
  </section>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  props: {
    first: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      pseudonym: ''
    }
  },

  methods: {
    ...mapActions('server', ['set_pseudonym_and_connect']),

    submit () {
      if (!this.pseudonym) {
        this.$refs.input.focus()
      } else {
        this.set_pseudonym_and_connect(this.pseudonym)
      }
    }
  },

  mounted () {
    const ls_pseudonym = localStorage.getItem('zestedecode-voxel-pseudonym')
    if (ls_pseudonym) {
      this.pseudonym = ls_pseudonym
    }

    if (this.$refs.input) {
      this.$refs.input.focus()
    }
  }
}
</script>

<style lang="sass">
@import "@/assets/main"

#welcome
  display: flex
  flex-direction: column
  justify-content: center
  align-items: center

  > header
    margin-bottom: 0

    border-bottom-left-radius: 0
    border-bottom-right-radius: 0

    width: 40%
    background: $primary

    text-align: center
    user-select: none

    img
      height: 3.2rem
      vertical-align: middle

  > div.box
    width: 64%

    +until-widescreen
      width: 84%

    padding: $length-16 $length-10

    article
      display: flex
      align-items: flex-start

      margin: 0 auto
      width: 90%

      +fullhd
        width: 666px

      &:nth-child(2n)
        flex-direction: row-reverse

        > figure
          margin-right: 0
          margin-left: $length-10

        > div
          display: flex
          flex-direction: column
          align-items: flex-end

          text-align: right

      &.is-pseudonym-form
        padding-top: $length-24
        border-top: solid $length-1 $grey-200

      & + article
        margin-top: $length-24

      > figure
        box-sizing: content-box

        margin-right: $length-10
        padding: $length-10
        border-radius: $radius-round

        background-color: $primary
        color: white

      &.is-link > figure
        background-color: $link

      > div
        > h2
          margin-bottom: $length-4

          font-size: 1.6rem
          line-height: 1.2

          color: $grey-900

        > p
          width: 90%

          font-size: 1.1rem
          color: $grey-800

          & + p, & + .field
            margin-top: $length-6
</style>
