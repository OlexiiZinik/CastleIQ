from loguru import logger
from config import conf

logger.level(conf.log_level)
