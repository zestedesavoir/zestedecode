function _get_message(message) {
  return typeof message === 'function' ? message() : message
}

export function log(out, message) {
    out('[' + (new Date().toISOString()) + '] ' + _get_message(message))
}

export function log_info(message) {
    log(console.log, '[INFO] ' + _get_message(message))
}

export function log_err(message) {
    log(console.error, '[ERROR] ' + _get_message(message))
}

export function log_debug(message) {
  if ((process.env.NODE_ENV || 'development') != 'production') {
    log(console.debug, '[DEBUG] ' + _get_message(message));
  }
}
