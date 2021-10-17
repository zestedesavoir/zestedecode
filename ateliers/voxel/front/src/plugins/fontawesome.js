import Vue from 'vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import {
  faCaretDown,
  faCaretUp,
  faCheckCircle as faCheckCircleSolid,
  faPlay,
  faExclamationCircle,
  faColumns,
  faCubes,
  faHandsHelping,
  faBug,
  faAngleRight,
  faAngleDoubleRight,
  faAngleDoubleLeft,
  faLaptopCode,
  faChalkboardTeacher,
  faSignature,
  faExternalLinkAlt,
  faHome,
  faArrowRight,
  faArrowLeft
} from '@fortawesome/free-solid-svg-icons'

import {
  faCheckCircle,
  faDotCircle,
  faWindowMaximize,
  faCommentDots,
  faKeyboard
} from '@fortawesome/free-regular-svg-icons'

import {
  faMarkdown
} from '@fortawesome/free-brands-svg-icons'

library.add(
  faCaretDown,
  faCaretUp,
  faPlay,
  faCheckCircleSolid,
  faCheckCircle,
  faExclamationCircle,
  faDotCircle,
  faColumns,
  faWindowMaximize,
  faCubes,
  faHandsHelping,
  faCommentDots,
  faBug,
  faKeyboard,
  faAngleRight,
  faAngleDoubleRight,
  faAngleDoubleLeft,
  faLaptopCode,
  faChalkboardTeacher,
  faSignature,
  faExternalLinkAlt,
  faHome,
  faArrowRight,
  faArrowLeft,
  faMarkdown
)

Vue.component('font-awesome-icon', FontAwesomeIcon)
