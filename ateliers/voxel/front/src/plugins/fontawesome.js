import Vue from 'vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import {
  faCaretDown,
  faCaretUp,
  faPlay,
  faExclamationCircle,
  faColumns,
  faCubes,
  faHandsHelping,
  faBug
} from '@fortawesome/free-solid-svg-icons'

import {
  faCheckCircle,
  faWindowMaximize,
  faCommentDots,
  faKeyboard
} from '@fortawesome/free-regular-svg-icons'

library.add(
  faCaretDown,
  faCaretUp,
  faPlay,
  faCheckCircle,
  faExclamationCircle,
  faColumns,
  faWindowMaximize,
  faCubes,
  faHandsHelping,
  faCommentDots,
  faBug,
  faKeyboard
)

Vue.component('font-awesome-icon', FontAwesomeIcon)
