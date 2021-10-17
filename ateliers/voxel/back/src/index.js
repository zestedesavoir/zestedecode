import http from "http"
import ZestVoxelServer from "./server"

import { log_info } from "./logging"

const SERVER_PORT = process.env.ZESTEDECODE_WS_PORT || 48506
const TEACHERS_PASSWORD = process.env.ZESTEDECODE_TEACHERS_PASSWORD || 'zeste'

let server = http.createServer(function(request, response) {
    if (request.url.startsWith("/munin")) return

    response.writeHead(404)
    response.end()
})

server.listen(SERVER_PORT, function() {
    log_info(`Server listening on port ${SERVER_PORT}.`)

    const voxel_server = new ZestVoxelServer(server)
    voxel_server.set_teachers_password(TEACHERS_PASSWORD)
    voxel_server.start()
})
