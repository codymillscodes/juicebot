import logging.handlers
import logging_loki

logging_loki.emitter.LokiEmitter.level_tag = "level"
# assign to a variable named handler 
handler = logging_loki.LokiHandler(
   url="https://205240:eyJrIjoiNjVhMDNlOGMwNWU4MmM0ZWZkYjQyMWNkOTZlZjdjNTg2NWRlNjYyMiIsIm4iOiJ3YWZmbGUiLCJpZCI6NjM5NTI1fQ==@logs-prod3.grafana.net/loki/api/v1/push",
   version="1",
)

# create a new logger instance, name it whatever you want
logger = logging.getLogger("waffle_log")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def log(level, cmd, msg):
    if level == 'debug':
        logger.debug(f"[{cmd}] {msg}")
    elif level == 'info':
        logger.info(f"[{cmd}] {msg}")
    elif level == 'warning':
        logger.warning(f"[{cmd}] {msg}")
    elif level == 'error':
        logger.error(f"[{cmd}] {msg}")
    elif level == 'critical':
        logger.critical(f"[{cmd}] {msg}")
    else:
        logger.error(f"Failed to log, likely due to misspelling the level.")
