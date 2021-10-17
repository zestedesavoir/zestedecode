<template>
  <b-dropdown
    aria-role="list"
    position="is-bottom-left"
    class="level-item users-list"
    :class="{'is-teacher': teacher}">

    <button class="button" :class="{'is-outlined': teacher, 'is-primary': !teacher, 'is-white': teacher}" slot="trigger" slot-scope="{ active }">
      <span v-if="!teacher">{{ users_online_count }} en ligne</span>
      <div v-else>
        <h3>Contexte</h3>
        <p>Votre participation</p>
      </div>
      <b-icon :icon="active ? 'caret-up' : 'caret-down'" />
    </button>

    <b-dropdown-item custom aria-role="listitem" v-if="teacher">
      <strong>Cliquez sur un participant ci-dessous</strong> pour voir
       son code en temps réel et répondre aux demandes d'aide.<br />
      Cliquez sur votre propre nom pour revenir à votre participation.
    </b-dropdown-item>

    <hr class="dropdown-divider" v-if="teacher" />

    <div v-for="(category, i) in users_sorted" :key="i">
      <b-dropdown-item custom class="is-user-group-title" v-if="category.length > 0">
        {{ i === 'teachers' ? 'Organisateurs' : 'Participants' }}
      </b-dropdown-item>

      <b-dropdown-item :custom="!teacher" aria-role="listitem" v-for="(user, j) in category" :key="i + j">
        <div class="media">
          <div class="media-left">
            <online :online="user.online" />
          </div>
          <div class="media-content is-user-status">
            <p>{{ user.pseudonym}}</p>
            <p  v-if="!user.online && teacher"><small>Vu à {{ user.last_seen_at }}</small></p>
          </div>
          <div class="media-right" v-if="teacher">
            <b-tag rounded type="is-warning">1</b-tag>
          </div>
        </div>
      </b-dropdown-item>

      <hr class="dropdown-divider" v-if="i !== 'users' && category.length > 0"/>
    </div>
  </b-dropdown>
</template>

<script>
import { mapState } from 'vuex'

import Online from '../elements/Online.vue'

export default {
  computed: {
    ...mapState('server', ['users', 'teacher']),

    users_online_count () {
      return Object.values(this.users).filter(user => user.online).length
    },

    users_sorted () {
      const sort_users_fn = (a, b) => a.online === b.online ? a.pseudonym.localeCompare(b.pseudonym) : (a.online ? -1 : 1)

      const users = Object.values(this.users).reduce(
        (acc, user) => { (user.teacher ? acc.teachers : acc.users).push(user); return acc },
        { teachers: [], users: [] }
      )

      users.teachers.sort(sort_users_fn)
      users.users.sort(sort_users_fn)

      return users
    }
  },

  components: {
    Online
  }
}
</script>

<style lang="sass">
@import '@/assets/main'

div.dropdown.users-list
  .dropdown-menu
    .dropdown-item
        .media
          align-items: center

  &.is-teacher
    margin-left: $length-4

    .dropdown-trigger button
      padding-top: 0
      padding-bottom: 0

      &:hover, &:focus, &:active
        border-color: white
        background-color: $primary-700
        color: white

      div
        align-self: end
        text-align: left

        h3
          font-size: .8rem
          line-height: .5
        p
          font-size: 1.16rem
          line-height: 1.4

    .dropdown-menu
      +desktop
        width: $length-256

      .dropdown-item
        padding-right: 1rem
        white-space: initial !important

        .tag
          font-weight: bold

        &:hover .tag
          background-color: $primary-000
          color: $primary-800
</style>
