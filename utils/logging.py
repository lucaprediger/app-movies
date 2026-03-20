import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:    %(message)s",
    force=True
)

logger = logging.getLogger("app_movies")