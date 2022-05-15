import logging.handlers
import logging_loki
from multiprocessing import Queue


handler = logging_loki.LokiQueueHandler(
    Queue(-1),
    url="http://192.168.1.76:3100/loki/api/v1/push", 
    tags={"application": "waffle"}
)

logger = logging.getLogger("my-logger")
logger.addHandler(handler)

def loggi(line, msg, tag):
    logger.error(f"[{line}]: {msg}", extra={"tags": {"command": tag}})