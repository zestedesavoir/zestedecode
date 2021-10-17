import { log_info } from "../logging"

export class Game {
  constructor(slug, server, seed) {
    this.server = server

    this.seed = seed || Math.round(Math.random() * 1000000000000000)

    this.entities = {}
    this.players = {}

    // TODO (voxel server-side stuff, etc.)
  }

  log(message) {
    log_info("[" + this.slug + "] " + message)
  }
}
